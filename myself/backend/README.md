# K8s Ingress 测试后端

这是一个简单的Python后端服务，用于测试Kubernetes的Ingress功能，特别是不同URL路径到不同后端的路由功能。

## 文件说明

- `backend.py`: Flask应用程序，提供多个URL路径的API接口
- `requirements.txt`: Python依赖包列表
- `Dockerfile`: 用于构建Docker镜像
- `k8s-deploy.yaml`: 单一后端服务的Kubernetes部署和服务定义
- `k8s-multi-deploy.yaml`: 多个后端服务的Kubernetes部署和服务定义
- `ingress.yaml`: 基本Ingress资源示例
- `multi-ingress.yaml`: 多路径和子域名Ingress资源示例

## API路径

服务提供以下API路径用于测试:

- `/`: 根路径，返回服务信息
- `/api`: 基本API路径
- `/api/v1/users`: 用户API V1版本
- `/api/v1/products`: 产品API V1版本
- `/api/v2/status`: 状态API V2版本
- `/app/dashboard`: 仪表板应用路径
- `/health`: 健康检查路径
- `/<任意路径>`: 通配符路径处理器，返回请求路径和头信息

## 使用方法

### 构建Docker镜像

```bash
cd myself/backend
docker build -t your-registry/ingress-test-backend:latest .
docker push your-registry/ingress-test-backend:latest
```

### 部署单一后端服务

```bash
# 修改k8s-deploy.yaml中的镜像地址
kubectl apply -f k8s-deploy.yaml
kubectl apply -f ingress.yaml
```

### 部署多后端服务测试环境

```bash
# 修改k8s-multi-deploy.yaml中的镜像地址
kubectl apply -f k8s-multi-deploy.yaml
kubectl apply -f multi-ingress.yaml
```

### 测试路径路由

使用curl或浏览器访问不同的路径，验证Ingress路由是否正确:

```bash
# 基于路径的路由测试
curl http://test.example.com/api/v1/users
curl http://test.example.com/api/v2/status
curl http://test.example.com/app/dashboard

# 基于子域名的路由测试
curl http://api.example.com/api/v1/users
curl http://status.example.com/api/v2/status
curl http://dashboard.example.com/app/dashboard
```

预期的响应中会包含路径信息和主机名，这样可以确认请求路由到了正确的后端服务:

```json
{
  "hostname": "api-service-5d7769c7b9-abcde",
  "message": "User API - Version 1",
  "pod_ip": "10.244.0.15",
  "path": "/api/v1/users",
  "data": [
    {"id": 1, "name": "User 1"},
    {"id": 2, "name": "User 2"}
  ]
}
```

## Ingress路由规则说明

- 路径前缀路由:
  - `/api/v1/*` 路由到 `api-service`
  - `/api/v2/*` 路由到 `status-service`
  - `/app/*` 路由到 `dashboard-service`
  
- 子域名路由:
  - `api.example.com` 路由到 `api-service`
  - `status.example.com` 路由到 `status-service`
  - `dashboard.example.com` 路由到 `dashboard-service`

## 测试技巧

1. 使用`kubectl get ingress`查看Ingress状态
2. 使用`kubectl describe ingress <name>`检查Ingress详情
3. 检查Ingress Controller日志排查问题
4. 临时修改本地hosts文件以便测试子域名路由 