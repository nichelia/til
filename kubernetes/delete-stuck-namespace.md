# Delete Stuck Namespace

## Description

I encountered instances where a namespace on a Kubernetes cluster, would get stuck on `Terminating` state.

This often happend when I installed/uninstalled Kubeflow (v.1) on an AWS EKS cluster (v1.15).

Usually this state is reached when Kubernetes cluster fails to remove some resources.

## Resolution

* Identify stuck namespace (look for `Terminating` status).

```bash
kubectl get ns
```

* Gather resources failing to be removed.  
Replace `<namespace-name>` with your stuck namespace name (e.g. `default`).

```bash
NAMESPACE=<namespace-name>
kubectl api-resources --verbs=list --namespaced -o name | xargs -n 1 kubectl get --show-kind --show-all --ignore-not-found -n $NAMESPACE
```

* Debug `"unable to retrieve the complete list of server APIs: <api-resource>/<version>: the server is currently unable to handle the request"` message.  
Replace `<version>.<api-resource>` with the API Service (e.g. `custom.metrics.k8s.io/v1beta1`).

```bash
kubectl get APIService <version>.<api-resource>
kubectl describe APIService <version>.<api-resource>
```

* Retrieve namespace contents.

```bash
kubectl get ns $NAMESPACE -o json > /tmp/${NAMESPACE}.json
```

* Edit contents to remove all elements in finalizer array, leaving only an empty array `[]` (e.g. `"finalizers": []`).

```bash
vi /tmp/${NAMESPACE}.json
```

* Use proxy to push changes via `curl`.

```bash
kubectl proxy &
curl -k -H "Content-Type: application/json" -X PUT --data-binary @/tmp/${NAMESPACE}.json http://127.0.0.1:8001/api/v1/namespaces/$NAMESPACE/finalize
```

* Verify deletion of namespace - it should not be in the output list.

```bash
kubectl get ns
```

## References:
- [Docker - How to Delete a Kubernetes Namespace Stuck in the Terminating State](https://success.docker.com/article/kubernetes-namespace-stuck-in-terminating)
- [IBM - A namespace is stuck in the Terminating state](https://www.ibm.com/support/knowledgecenter/SSBS6K_3.2.0/troubleshoot/ns_terminating.html)