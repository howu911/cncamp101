import ray
from ray import serve
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# 1. 启动或连接 Ray
# ray.init(address='ray://10.90.30.198:10001')  # 如果你已经在外部启动了Ray，也可以使用 ray.init(address="auto") 连接集群
ray.init()

@serve.deployment(route_prefix="/sentiment", num_replicas=1)
class SentimentAnalyzer:
    def __init__(self):
        # 2. 直接使用本地已下载的模型和分词器
        model_path = "/home/laijiatao/code/github/k8s/cncamp101/myself/ray_stu/ray_serve/distilbert-base-uncased-finetuned-sst-2-english"
        print(f"Loading local model from: {model_path}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True, use_safetensors=False, trust_remote_code=True, revision="main")
        self.model.eval()  # 设置推理模式

    async def __call__(self, request):
        # 3. 从请求中获取文本
        data = await request.json()
        text = data.get("text", "")
        
        # 简单检查
        if not text:
            return {"error": "No text provided."}
        
        # 4. 模型推理
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
        
        # 5. 获取预测结果
        probs = F.softmax(logits, dim=-1).cpu().numpy()[0]
        # distilbert-base-uncased-finetuned-sst-2-english 的标签顺序一般是 [NEGATIVE, POSITIVE]
        negative_score, positive_score = probs
        label = "POSITIVE" if positive_score > negative_score else "NEGATIVE"
        confidence = float(max(negative_score, positive_score))

        return {
            "text": text,
            "label": label,
            "confidence": confidence
        }

# 6. 推荐使用 serve.run() 启动服务（Ray 2.0+）
app = SentimentAnalyzer.bind()

if __name__ == "__main__":
    serve.run(app)
    # 阻塞保持服务运行
    import time
    while True:
        time.sleep(1)
