# Minikube deep guide and how it differs from global kubectl

## 1) What Minikube is

Minikube is a local Kubernetes environment that runs a real Kubernetes cluster on your machine (inside Docker or a VM).

For this lab, Minikube gives you:
- A fast local control-plane node
- Simple cluster lifecycle commands (`start`, `stop`, `delete`)
- Easy profile isolation (you can have multiple local clusters)
- A built-in way to run kubectl without installing kubectl globally

In your setup, Minikube is using the Docker driver with profile `lab5`.

---

## 2) Core Minikube concepts

### Profile
A profile is a named cluster environment.

Example:
```bash
minikube start --driver=docker --cpus=2 --memory=3072 --profile=lab5
```

Here, `lab5` is the profile name.

### Driver
The driver is how Minikube runs Kubernetes (Docker, KVM, VirtualBox, etc.).

You are using:
```bash
--driver=docker
```

### Node count
By default Minikube starts one node. You can run more:
```bash
minikube start --profile=lab5 --nodes=3 --driver=docker --cpus=2 --memory=3072
```

---

## 3) Important Minikube commands (practical)

## Cluster lifecycle
```bash
minikube start --profile=lab5 --driver=docker --cpus=2 --memory=3072
minikube status -p lab5
minikube stop -p lab5
minikube delete -p lab5
minikube profile list
```

## Inspect cluster
```bash
minikube -p lab5 ip
minikube -p lab5 kubectl -- get nodes -o wide
minikube -p lab5 kubectl -- get pods -A
```

## Node management (multi-node profile)
```bash
minikube node add -p lab5
minikube node list -p lab5
minikube node delete <node-name> -p lab5
```

## Addons
```bash
minikube -p lab5 addons list
minikube -p lab5 addons enable metrics-server
minikube -p lab5 addons enable dashboard
minikube -p lab5 addons enable metallb
```

## Service access shortcuts
```bash
minikube -p lab5 service <service-name> --url
minikube -p lab5 tunnel
```

## Image workflows
```bash
minikube -p lab5 image load my-image:tag
minikube -p lab5 image ls
```

---

## 4) What `minikube ... kubectl -- ...` means

When you run:
```bash
minikube -p lab5 kubectl -- get pods
```
Minikube does 3 useful things for you:
1. Uses a kubectl version compatible with the cluster
2. Uses the profile kubeconfig context (`lab5`)
3. Runs the kubectl command after `--`

So even if `kubectl` is not installed globally, this still works.

---

## 5) Minikube kubectl wrapper vs global kubectl

| Topic | Minikube wrapper (`minikube -p lab5 kubectl -- ...`) | Global kubectl (`kubectl ...`) |
|---|---|---|
| Requires global kubectl install | No | Yes |
| Version matching with Minikube cluster | Automatic | You manage it |
| Context safety for local profile | Very safe (explicit `-p lab5`) | Depends on current kube-context |
| First-run speed | Slower (may download kubectl) | Faster once installed |
| Scripting ergonomics | More verbose command | Cleaner and standard |
| Multi-cluster daily ops | Less convenient | Better for frequent cluster switching |
| Works in your current machine state | Yes | No (kubectl missing globally) |

---

## 6) When to use which approach

Use Minikube wrapper when:
- You do not have global kubectl installed
- You want strict profile-scoped commands
- You are doing local lab work quickly

Use global kubectl when:
- You work across many clusters often
- You use kubectl plugins, scripts, CI jobs
- You want standard command syntax everywhere

---

## 7) Recommended workflow for this lab machine

Because your machine currently has no global kubectl, use this function in the terminal:

```bash
k() { minikube -p lab5 kubectl -- "$@"; }
```

Then run Kubernetes commands normally:
```bash
k get nodes
k get pods -A
k apply -f myfile.yaml
```

This is the cleanest way to work through exercises right now.

