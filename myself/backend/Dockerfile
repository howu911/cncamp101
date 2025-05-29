FROM python:3.9-slim

# 设置环境变量
ENV http_proxy=http://proxyhk.zte.com.cn:80
ENV https_proxy=http://proxyhk.zte.com.cn:80


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend.py .

EXPOSE 8080

CMD ["python", "backend.py"] 