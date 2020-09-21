# Get sorted events

## Description

Several times I found myself getting Kubernetes event logs (`kubectl get events`) unordered. Truth is the command does not return back the events in an ordered fashion.

## Resolution

* Append a sort by at the end of the command.

```bash
kubectl get events --sort-by='.metadata.creationTimestamp'
```

## References:
- [kubectl get events doesnt sort events by last seen time. #29838](https://github.com/kubernetes/kubernetes/issues/29838)
