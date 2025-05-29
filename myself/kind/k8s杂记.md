# 安装工具
apt install dnsutils -y


# bash补全
apt install bash-completion
echo '[[ $PS1 && -f /usr/share/bash-completion/bash_completion ]] && source /usr/share/bash-completion/bash_completion' >> ~/.bashrc
source ~/.bashrc
source <(kubectl completion bash)



# kind k8s组件日志路径
/var/log/containers/
## kubelet日志路径
journalctl -u kubelet -f


# 安装nerdctl
curl -LO https://github.com/containerd/nerdctl/releases/download/v1.7.6/nerdctl-1.7.6-linux-amd64.tar.gz
tar -xvf nerdctl-*.tar.gz
mv nerdctl /usr/local/bin/


# containerd配置镜像
## /etc/containerd/certs.d/docker.io/hosts.toml
```bash
server = "https://docker.io"

[host."https://docker.1ms.run"]
  capabilities = ["pull", "resolve"]

[host."https://docker.mybacc.com"]
  capabilities = ["pull", "resolve"]

[host."https://dytt.online"]
  capabilities = ["pull", "resolve"]

[host."https://lispy.org"]
  capabilities = ["pull", "resolve"]

[host."https://docker.xiaogenban1993.com"]
  capabilities = ["pull", "resolve"]

[host."https://docker.yomansunter.com"]
  capabilities = ["pull", "resolve"]

[host."https://aicarbon.xyz"]
  capabilities = ["pull", "resolve"]

[host."https://666860.xyz"]
  capabilities = ["pull", "resolve"]

[host."https://docker.zhai.cm"]
  capabilities = ["pull", "resolve"]

[host."https://a.ussh.net"]
  capabilities = ["pull", "resolve"]

[host."https://hub.littlediary.cn"]
  capabilities = ["pull", "resolve"]

[host."https://hub.rat.dev"]
  capabilities = ["pull", "resolve"]

[host."https://docker.m.daocloud.io"]
  capabilities = ["pull", "resolve"]
```

## /etc/containerd/config.toml
containerd config default > /etc/containerd/config.toml
systemctl daemon-reload
systemctl restart containerd
systemctl status containerd

```bash
[plugins."io.containerd.grpc.v1.cri".registry]
  config_path = "/etc/containerd/certs.d"
```

# 查看kube-proxy的配置
kubectl -n kube-system exec kube-proxy-dqz6g -- cat /var/lib/kube-proxy/config.conf

```bash
iptables -t nat -S | grep KUBE-SERVICES
-N KUBE-SERVICES
-A PREROUTING -m comment --comment "kubernetes service portals" -j KUBE-SERVICES
-A OUTPUT -m comment --comment "kubernetes service portals" -j KUBE-SERVICES


root@kind-cluster-worker2:~# iptables -t nat -S | grep 10.96.206.52
-A KUBE-SERVICES -d 10.96.206.52/32 -p tcp -m comment --comment "default/web-service cluster IP" -m tcp --dport 80 -j KUBE-SVC-SZGXCNNBZLC4E3DM
-A KUBE-SVC-SZGXCNNBZLC4E3DM ! -s 10.244.0.0/16 -d 10.96.206.52/32 -p tcp -m comment --comment "default/web-service cluster IP" -m tcp --dport 80 -j KUBE-MARK-MASQ


root@kind-cluster-worker2:~# iptables -t nat -S | grep KUBE-SVC-SZGXCNNBZLC4E3DM
-N KUBE-SVC-SZGXCNNBZLC4E3DM
-A KUBE-SERVICES -d 10.96.206.52/32 -p tcp -m comment --comment "default/web-service cluster IP" -m tcp --dport 80 -j KUBE-SVC-SZGXCNNBZLC4E3DM
-A KUBE-SVC-SZGXCNNBZLC4E3DM ! -s 10.244.0.0/16 -d 10.96.206.52/32 -p tcp -m comment --comment "default/web-service cluster IP" -m tcp --dport 80 -j KUBE-MARK-MASQ
-A KUBE-SVC-SZGXCNNBZLC4E3DM -m comment --comment "default/web-service -> 10.244.1.10:80" -m statistic --mode random --probability 0.33333333349 -j KUBE-SEP-LJSFUGXYHK6BOCVT
-A KUBE-SVC-SZGXCNNBZLC4E3DM -m comment --comment "default/web-service -> 10.244.1.11:80" -m statistic --mode random --probability 0.50000000000 -j KUBE-SEP-V64CEIOABZ4EVXRD
-A KUBE-SVC-SZGXCNNBZLC4E3DM -m comment --comment "default/web-service -> 10.244.1.9:80" -j KUBE-SEP-5B6VHRE3J4X6IDTW


root@kind-cluster-worker2:~# iptables -t nat -S | grep KUBE-SEP-LJSFUGXYHK6BOCVT
-N KUBE-SEP-LJSFUGXYHK6BOCVT
-A KUBE-SEP-LJSFUGXYHK6BOCVT -s 10.244.1.10/32 -m comment --comment "default/web-service" -j KUBE-MARK-MASQ
-A KUBE-SEP-LJSFUGXYHK6BOCVT -p tcp -m comment --comment "default/web-service" -m tcp -j DNAT --to-destination 10.244.1.10:80
-A KUBE-SVC-SZGXCNNBZLC4E3DM -m comment --comment "default/web-service -> 10.244.1.10:80" -m statistic --mode random --probability 0.33333333349 -j KUBE-SEP-LJSFUGXYHK6BOCVT
root@kind-cluster-worker2:~# iptables -t nat -S | grep KUBE-SEP-V64CEIOABZ4EVXRD
-N KUBE-SEP-V64CEIOABZ4EVXRD
-A KUBE-SEP-V64CEIOABZ4EVXRD -s 10.244.1.11/32 -m comment --comment "default/web-service" -j KUBE-MARK-MASQ
-A KUBE-SEP-V64CEIOABZ4EVXRD -p tcp -m comment --comment "default/web-service" -m tcp -j DNAT --to-destination 10.244.1.11:80
-A KUBE-SVC-SZGXCNNBZLC4E3DM -m comment --comment "default/web-service -> 10.244.1.11:80" -m statistic --mode random --probability 0.50000000000 -j KUBE-SEP-V64CEIOABZ4EVXRD
root@kind-cluster-worker2:~# iptables -t nat -S | grep KUBE-SEP-5B6VHRE3J4X6IDTW
-N KUBE-SEP-5B6VHRE3J4X6IDTW
-A KUBE-SEP-5B6VHRE3J4X6IDTW -s 10.244.1.9/32 -m comment --comment "default/web-service" -j KUBE-MARK-MASQ
-A KUBE-SEP-5B6VHRE3J4X6IDTW -p tcp -m comment --comment "default/web-service" -m tcp -j DNAT --to-destination 10.244.1.9:80
-A KUBE-SVC-SZGXCNNBZLC4E3DM -m comment --comment "default/web-service -> 10.244.1.9:80" -j KUBE-SEP-5B6VHRE3J4X6IDTW


```

# 安装nginx-ingress-controller
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm search repo ingress-nginx --versions
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --version 4.11.0
