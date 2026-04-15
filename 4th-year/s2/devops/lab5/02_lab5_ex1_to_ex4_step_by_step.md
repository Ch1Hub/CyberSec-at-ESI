# Lab 5 step-by-step commands (Exercises 1 to 5)

This guide uses your current environment (Minikube profile `lab5`) without global kubectl.

## 0) One-time setup in terminal

```bash
# 0.1 Start cluster if needed
minikube start --profile=lab5 --driver=docker --cpus=2 --memory=3072

# 0.2 Helper function so you can type `k ...`
k() { minikube -p lab5 kubectl -- "$@"; }

# 0.3 Quick health checks
k cluster-info
k get nodes -o wide
k get ns
```

---

## Exercise 1 - Pods

## 1. Create Pod `mypod` using nginx image
```bash
k run mypod --image=nginx:1.25 --restart=Never
```

## 2. Verify Pod status
```bash
k get pods
k get pods -o wide
```

## 3. Describe Pod details
```bash
k describe pod mypod
```

Optional checks:
```bash
k logs mypod
```

---

## Exercise 2 - Deployments, scaling, rollout, rollback

## 1. Create Deployment `nginx-deploy` with 3 replicas
```bash
k create deployment nginx-deploy --image=nginx:1.19 --replicas=3
```

## 2. Verify all pods are running
```bash
k get deploy nginx-deploy
k get pods -l app=nginx-deploy -o wide
```

## 3-4. Scale to 5 replicas and verify
```bash
k scale deployment nginx-deploy --replicas=5
k get deploy nginx-deploy
k get pods -l app=nginx-deploy
```

## 5-6. Delete one pod manually and observe self-healing
```bash
POD_TO_DELETE=$(k get pods -l app=nginx-deploy -o jsonpath='{.items[0].metadata.name}')
k delete pod "$POD_TO_DELETE"
k get pods -l app=nginx-deploy
```

## 7. Update image versions (1.19 -> 1.21 -> 1.25)
```bash
k set image deployment/nginx-deploy nginx=nginx:1.21
k rollout status deployment/nginx-deploy

k set image deployment/nginx-deploy nginx=nginx:1.25
k rollout status deployment/nginx-deploy
```

## 8. Check rollout status
```bash
k rollout status deployment/nginx-deploy
```

## 9. Check rollout revisions/history
```bash
k rollout history deployment/nginx-deploy
```

## 10. Rollback to previous version
```bash
k rollout undo deployment/nginx-deploy
k rollout status deployment/nginx-deploy
k rollout history deployment/nginx-deploy
```

## 11. Delete deployment (as asked in exercise)
```bash
k delete deployment nginx-deploy
```

---

## Exercise 3 - Services

Exercise 2 ends by deleting the deployment, so recreate it first:

```bash
k create deployment nginx-deploy --image=nginx:1.25 --replicas=3
k get pods -l app=nginx-deploy
```

## 1. Expose deployment with ClusterIP service
```bash
k expose deployment nginx-deploy \
  --name=nginx-clusterip \
  --type=ClusterIP \
  --port=8080 \
  --target-port=80
```

## 2. Create NodePort service
```bash
k expose deployment nginx-deploy \
  --name=nginx-nodeport \
  --type=NodePort \
  --port=8081 \
  --target-port=80
```

## 3. Verify access to both services

Inspect services:
```bash
k get svc nginx-clusterip nginx-nodeport -o wide
```

Test ClusterIP from inside cluster:
```bash
k run curltest --image=curlimages/curl:8.7.1 --rm -i --restart=Never -- \
  sh -c "curl -s nginx-clusterip:8080 | head -n 3"
```

Test NodePort from host:
```bash
NODE_IP=$(minikube -p lab5 ip)
NODE_PORT=$(k get svc nginx-nodeport -o jsonpath='{.spec.ports[0].nodePort}')
curl -s "http://$NODE_IP:$NODE_PORT" | head -n 3
```

---

## Exercise 4 - Namespaces

## 1. List existing namespaces
```bash
k get namespaces
```

## 2. Create `dev` and `prod` using two different methods

Method A (CLI) for `dev`:
```bash
k create namespace dev
```

Method B (YAML) for `prod`:
```bash
cat > prod-namespace.yaml <<'EOF'
apiVersion: v1
kind: Namespace
metadata:
  name: prod
EOF

k apply -f prod-namespace.yaml
```

## 3. Deploy nginx deployment + service in both namespaces

Deploy to `dev`:
```bash
k -n dev create deployment nginx-deploy --image=nginx:1.25 --replicas=3
k -n dev expose deployment nginx-deploy --name=nginx-svc --type=ClusterIP --port=80 --target-port=80
```

Deploy to `prod`:
```bash
k -n prod create deployment nginx-deploy --image=nginx:1.25 --replicas=3
k -n prod expose deployment nginx-deploy --name=nginx-svc --type=ClusterIP --port=80 --target-port=80
```

## 4. List all pods and services in both namespaces
```bash
k -n dev get pods,svc -o wide
k -n prod get pods,svc -o wide
```

Cross-check all namespaces:
```bash
k get pods -A
k get svc -A
```

---

## Exercise 5 - Custom Node.js app + rollout + LoadBalancer (your exact setup)

Your machine has very low disk space, so these steps are adapted to **not** run a host private registry.
Instead, we use: `docker build` + `minikube image load`.

This section uses:
`~/Documents/cys2CS/s2/devOps/lab5/nodeapp`

## 1. Build and deploy v1 in namespace `dev-node` (2 replicas)
```bash
cd ~/Documents/cys2CS/s2/devOps/lab5/nodeapp
k() { minikube -p lab5 kubectl -- "$@"; }

# Make deployment match your local-image workflow (no registry)
sed -i 's#image: .*#image: node-app-image:v1#' k8s/nodeapp-deployment.yaml
sed -i 's/imagePullPolicy: Always/imagePullPolicy: IfNotPresent/' k8s/nodeapp-deployment.yaml

# Build image and load it into minikube
docker build -t node-app-image:v1 .
minikube -p lab5 image load node-app-image:v1

# Deploy
k apply -f k8s/dev-node-namespace.yaml
k apply -f k8s/nodeapp-deployment.yaml
k apply -f k8s/nodeapp-service-nodeport.yaml

# Verify
k -n dev-node get deploy,pods,svc -o wide
NODE_IP=$(minikube -p lab5 ip)
curl -s "http://$NODE_IP:30090"
```

## 2. Create and deploy v2 (code change + rollout)
```bash
cd ~/Documents/cys2CS/s2/devOps/lab5/nodeapp
perl -0pi -e 's/version: appVersion,/version: appVersion,\n      release: "v2",/' server.js

docker build -t node-app-image:v2 .
minikube -p lab5 image load node-app-image:v2

k -n dev-node set image deployment/node-app-deploy node-app=node-app-image:v2
k -n dev-node rollout status deployment/node-app-deploy
k -n dev-node rollout history deployment/node-app-deploy
curl -s "http://$NODE_IP:30090"
```

## 3. Create and deploy v3 (another code change + rollout)
```bash
cd ~/Documents/cys2CS/s2/devOps/lab5/nodeapp
sed -i 's/release: "v2"/release: "v3"/' server.js

docker build -t node-app-image:v3 .
minikube -p lab5 image load node-app-image:v3

k -n dev-node set image deployment/node-app-deploy node-app=node-app-image:v3
k -n dev-node rollout status deployment/node-app-deploy
k -n dev-node rollout history deployment/node-app-deploy
curl -s "http://$NODE_IP:30090"
```

## 4. Rollback
```bash
k -n dev-node rollout undo deployment/node-app-deploy
k -n dev-node rollout status deployment/node-app-deploy
k -n dev-node rollout history deployment/node-app-deploy
curl -s "http://$NODE_IP:30090"
```

## 5. Create LoadBalancer service with MetalLB
Enable MetalLB:
```bash
minikube -p lab5 addons enable metallb
```

Create address pool + L2 advertisement:
```bash
cat > k8s/metallb-pool.yaml <<'EOF'
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: first-pool
  namespace: metallb-system
spec:
  addresses:
    - 192.168.49.240-192.168.49.250
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: l2adv
  namespace: metallb-system
spec:
  ipAddressPools:
    - first-pool
EOF

k apply -f k8s/metallb-pool.yaml
```

Deploy LoadBalancer service and test:
```bash
k apply -f k8s/nodeapp-service-loadbalancer.yaml
k -n dev-node get svc node-app-svc-lb -w

LB_IP=$(k -n dev-node get svc node-app-svc-lb -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -s "http://$LB_IP"
```

---

## Useful cleanup commands (after lab)

```bash
k delete pod mypod --ignore-not-found
k delete ns dev prod dev-node --ignore-not-found
k delete svc nginx-clusterip nginx-nodeport --ignore-not-found
k delete deployment nginx-deploy --ignore-not-found
rm -f prod-namespace.yaml
rm -f ~/Documents/cys2CS/s2/devOps/lab5/nodeapp/k8s/metallb-pool.yaml
```
