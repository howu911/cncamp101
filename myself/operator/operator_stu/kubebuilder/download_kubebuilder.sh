version="v4.3.1"
curl -L -o kubebuilder "https://github.com/kubernetes-sigs/kubebuilder/releases/download/${version}/kubebuilder_$(go env GOOS)_$(go env GOARCH)"
chmod +x kubebuilder && mv kubebuilder /usr/local/bin/
