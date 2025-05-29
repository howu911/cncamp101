# 清除代理环境变量
unset http_proxy
unset https_proxy
unset HTTP_PROXY
unset HTTPS_PROXY

# 调用原始curl命令
curl "$@"
