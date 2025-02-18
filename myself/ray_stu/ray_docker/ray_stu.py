import ray
import time

# 初始化 Ray
ray.init(address='ray://10.90.30.198:10001')  # 连接到现有的 Ray 集群

@ray.remote
def compute_square(number):
    """计算数字的平方"""
    time.sleep(1)  # 模拟耗时操作
    return number * number

def compute_square_normal(number):
    """普通函数版本的计算平方"""
    time.sleep(1)  # 模拟耗时操作
    return number * number

def main():
    numbers = list(range(1, 11))  # 增加计算量到10个数字
    
    # 测试串行计算
    print("开始串行计算...")
    start_time = time.time()
    normal_results = [compute_square_normal(num) for num in numbers]
    serial_time = time.time() - start_time
    print(f"串行计算结果: {normal_results}")
    print(f"串行计算耗时: {serial_time:.2f} 秒")
    
    # 测试Ray并行计算
    print("\n开始Ray并行计算...")
    start_time = time.time()
    futures = [compute_square.remote(num) for num in numbers]
    ray_results = ray.get(futures)
    parallel_time = time.time() - start_time
    print(f"并行计算结果: {ray_results}")
    print(f"并行计算耗时: {parallel_time:.2f} 秒")
    
    # 计算加速比
    speedup = serial_time / parallel_time
    print(f"\n加速比: {speedup:.2f}x")
    print(f"性能提升: {(speedup-1)*100:.1f}%")

if __name__ == "__main__":
    main()