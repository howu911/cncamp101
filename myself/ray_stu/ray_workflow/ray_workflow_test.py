import ray
from ray import workflow
import random

##############################
#        工具函数:分块数据       #
##############################
def chunk_data(data, chunk_size):
    """将列表 data 按照 chunk_size 分块生成。"""
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]

##############################
#    1. 拉取并清洗数据 (Step)   #
##############################
@workflow.step
def fetch_and_clean_data():
    """
    演示用：模拟从外部获取原始数据，并执行简单的清洗。
    在实际业务中可替换成读取数据库、文件或API等过程。
    """
    # 这里生成一些随机数据，范围在1~5之间
    raw_data = [random.randint(1, 5) for _ in range(10)]
    print(f"[fetch_and_clean_data] Raw data: {raw_data}")

    # 简单模拟清洗：过滤掉值为 1 的“脏数据”
    cleaned_data = [x for x in raw_data if x != 1]
    print(f"[fetch_and_clean_data] Cleaned data: {cleaned_data}")
    return cleaned_data

#####################################
# 2. 分块预处理 & 聚合 (带循环/并行)  #
#####################################
@workflow.step
def preprocess_chunk(data_chunk):
    """
    对单个分块进行示例化的“预处理”。
    演示中只做一次求和，实际业务中可做更复杂的操作。
    """
    result = sum(data_chunk)
    print(f"  [preprocess_chunk] chunk={data_chunk}, sum={result}")
    return result

@workflow.step
def aggregate_preprocessed_data(partial_sums):
    """
    将多个分块的结果聚合到一起，这里仅做一次求和。
    """
    total_sum = sum(partial_sums)
    print(f"[aggregate_preprocessed_data] partial_sums={partial_sums}, total_sum={total_sum}")
    return total_sum

def create_preprocess_workflow(cleaned_data_step, chunk_size=3):
    """
    将“分块预处理”串成一个子工作流：
    1) 将 cleaned_data 分块
    2) 并行执行 preprocess_chunk
    3) 聚合所有分块结果
    """
    # 由于 cleaned_data_step 是一个工作流引用，需要在运行时获取其值
    # Ray Workflow 的方式：先返回一些 workflow steps，再组合。
    @workflow.step
    def split_data_step(cleaned_data):
        # 普通Python函数无法直接操作 workflow 里的引用数据，所以这里先定义一个step来做数据拆分
        chunk_list = list(chunk_data(cleaned_data, chunk_size))
        return chunk_list

    # 先将 cleaned_data 拆分为多个 chunk
    splitted_step = split_data_step.step(cleaned_data_step)

    # 对所有 chunk 创建并行预处理 Step
    @workflow.step
    def parallel_preprocess(chunks):
        tasks = [preprocess_chunk.step(c) for c in chunks]
        return workflow.continuation(aggregate_preprocessed_data.step(tasks))

    # 返回一个“聚合后结果”的 Step
    final_aggregated_step = parallel_preprocess.step(splitted_step)
    return final_aggregated_step

###########################################
# 3. 条件分支：根据数据结果决定使用哪个模型       #
###########################################
@workflow.step
def decide_model_path(aggregated_result):
    """
    简单逻辑：若数据总和大于 15 则走主模型，否则走备用模型。
    """
    if aggregated_result > 15:
        return "main_model"
    else:
        return "backup_model"

@workflow.step
def run_main_model(aggregated_result):
    """
    假设这是主模型推理。
    演示中只返回一个字符串和 aggregated_result，以示区别。
    """
    recs = f"MainRecs_{aggregated_result}"
    print(f"[run_main_model] => {recs}")
    return recs

@workflow.step
def run_backup_model(aggregated_result):
    """
    假设这是备用模型推理。
    """
    recs = f"BackupRecs_{aggregated_result}"
    print(f"[run_backup_model] => {recs}")
    return recs

@workflow.step
def conditional_merge(model_path, main_output, backup_output):
    """
    合并条件分支结果，最终只返回一个结果给下游。
    """
    if model_path == "main_model":
        print(f"[conditional_merge] Using main model output: {main_output}")
        return main_output
    else:
        print(f"[conditional_merge] Using backup model output: {backup_output}")
        return backup_output

###################################
# 4. 结果验证 (含重试机制) + 继续流程 #
###################################
@workflow.step(max_retries=2)
def validate_recommendations(recommendations):
    """
    验证结果是否满足一定业务规则；若验证不通过会抛异常触发自动重试。
    在演示中：如果是 "BackupRecs" 则抛异常，模拟验证失败。
    """
    if "BackupRecs" in recommendations:
        raise ValueError(f"[validate_recommendations] Failed. {recommendations} not acceptable!")
    print(f"[validate_recommendations] Passed => {recommendations}")
    # 返回推荐结果原文，方便后续使用
    return recommendations

##############################
# 5. 持久化结果 (或通知下游)    #
##############################
@workflow.step
def persist_results(recommendations):
    """
    将结果持久化到数据库、对象存储或发往下游。
    演示中只打印。
    """
    print(f"[persist_results] Final result => {recommendations}")
    return f"Persisted: {recommendations}"

##########################
# 最终：组装主工作流 & 运行  #
##########################
def main_workflow():
    """ 将上述所有步骤组装为一个完整的工作流。 """
    # 1) 拉取并清洗数据
    cleaned_step = fetch_and_clean_data.step()

    # 2) 分块预处理并聚合
    aggregated_step = create_preprocess_workflow(cleaned_step, chunk_size=3)

    # 3) 根据聚合结果决定模型分支
    model_path_step = decide_model_path.step(aggregated_step)
    main_recs_step = run_main_model.step(aggregated_step)
    backup_recs_step = run_backup_model.step(aggregated_step)
    final_recs_step = conditional_merge.step(model_path_step, main_recs_step, backup_recs_step)

    # 4) 验证推荐结果 + 重试
    validated_step = validate_recommendations.step(final_recs_step)

    # 5) 持久化结果
    persisted_step = persist_results.step(validated_step)

    # 返回最后一个 step
    return persisted_step

if __name__ == "__main__":
    # 1. 初始化 Ray
    ray.init()          # 或者指定地址等
    workflow.init()     # 初始化 Workflow

    # 2. 构建并运行工作流
    final_ref = main_workflow().run()

    # 3. 打印最终结果
    print("Workflow finished with result:", final_ref)
