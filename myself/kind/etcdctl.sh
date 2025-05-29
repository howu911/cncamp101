apt update && apt install -y etcd-client

export ETCDCTL_API=3
export ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.crt
export ETCDCTL_CERT=/etc/kubernetes/pki/etcd/server.crt
export ETCDCTL_KEY=/etc/kubernetes/pki/etcd/server.key
export ETCDCTL_ENDPOINTS=https://127.0.0.1:2379

etcdctl endpoint health


# 查询所有的key
etcdctl get / --prefix --keys-only 

# 查询key所对应的值
