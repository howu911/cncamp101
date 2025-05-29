# Kubernetes Gateway API 实现指南

本文档介绍如何使用 Kubernetes Gateway API 替代传统的 Ingress 资源来实现高级流量路由功能。

## Gateway API 简介

Gateway API 是 Kubernetes 中用于服务网络的下一代 API，它是 Ingress API 的继任者，提供了更强大、更灵活的流量路由能力。相比 Ingress，Gateway API：

- 更具表现力：支持更多的流量路由场景
- 更具扩展性：明确的扩展点
- 分离关注点：资源模型按职责划分
- 改进的类型安全性：更严格的验证

## 资源类型说明

Gateway API 使用以下几种主要资源类型：

1. **GatewayClass**: 定义网关控制器的行为，类似于 IngressClass
example.com/gateway-controller是Gateway API中GatewayClass资源的controllerName字段的值，这个值表示实现这个GatewayClass的控制器的名称。
在Gateway API架构中：
controllerName是一个特定格式的字符串，通常采用域名格式（如example.com/gateway-controller）
它用于标识哪个控制器负责处理这个GatewayClass定义的网关
每个Gateway API实现（如Istio、Contour、Traefik等）都会定义自己的controllerName
这个示例中的example.com/gateway-controller只是一个占位符。在实际部署时，您需要将其替换为您集群中实际安装的Gateway控制器的名称。
例如，几个常见的Gateway控制器的controllerName值：
Istio: istio.io/gateway-controller
Contour: gateway.networking.k8s.io/contour
Traefik: traefik.io/gateway-controller
Nginx Gateway: gateway.nginx.org/nginx-gateway-controller
要使Gateway API配置生效，您需要：
确保安装了Gateway API CRDs
安装支持Gateway API的控制器（如Istio、Contour等）
修改GatewayClass中的controllerName为您安装的具体控制器名称
2. **Gateway**: 定义特定网络入口点，相当于 Ingress Controller
3. **HTTPRoute**: 定义 HTTP 流量的路由规则，相当于 Ingress 资源

## 安装 Gateway API CRDs

在使用 Gateway API 之前，需要先安装 Gateway API CRDs：

```bash
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.0.0/standard-install.yaml
```

## 配置说明

我们的配置文件 `gateway-api.yaml` 实现了以下功能：

### 1. 基于路径的路由

通过单个 HTTPRoute 资源，根据不同的 URL 路径将流量路由到不同的后端服务：

- `/api/v1/*` → `api-service`
- `/api/v2/*` → `status-service`
- `/app/*` → `dashboard-service`
- `/` → `api-service`（默认路由）

### 2. 基于子域名的路由

通过多个 HTTPRoute 资源，根据不同的子域名将流量路由到不同的后端服务：

- `api.example.com` → `api-service`
- `status.example.com` → `status-service`
- `dashboard.example.com` → `dashboard-service`

## 部署指南

1. 确保集群中已安装 Gateway API CRDs
2. 部署 Gateway API 控制器（如 Contour、Istio 或其他支持 Gateway API 的控制器）
3. 应用配置文件：

```bash
kubectl apply -f gateway-api.yaml
```

4. 验证部署状态：

```bash
kubectl get gatewayclass,gateway,httproute
```

## 与传统 Ingress 对比

| 功能 | Ingress API | Gateway API |
|------|------------|------------|
| 路径路由 | 支持但有限 | 更灵活，支持更多匹配条件 |
| 流量拆分 | 需要注解实现 | 原生支持 |
| 请求修改 | 通过注解实现 | 通过标准化 Filter 实现 |
| 类型安全 | 有限 | 更严格 |
| 扩展点 | 不明确，通过注解 | 明确定义的扩展点 |

## 注意事项

1. Gateway API 仍在快速发展中，不同版本间可能有变化
2. 确保使用的 Gateway 控制器与你使用的 Gateway API 版本兼容
3. 相比 Ingress，Gateway API 资源间的关系更加复杂，需要更仔细地规划和管理

## 常见问题排查

如果遇到路由问题，可以按照以下步骤排查：

1. 确认 Gateway 状态是否为 Ready：`kubectl get gateway`
2. 检查 HTTPRoute 是否被正确接受：`kubectl get httproute -o wide`
3. 查看 Gateway 控制器日志：`kubectl logs -n <namespace> <gateway-controller-pod>`
4. 确认后端服务是否正常运行：`kubectl get pods,svc` 