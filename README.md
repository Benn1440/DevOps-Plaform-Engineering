# DevOps-Plaform-Engineering
This is a comprehensive and advanced DevOps/Platform Engineering task that touches on modern cloud-native patterns.

# Overview of the Components & Their Roles
- Kubernetes Cluster: The foundation. I'd use minikube for local development.

- Apache APISIX: Sits at the edge as the API Gateway and load balancer, routing external traffic to our services.

- Dapr: The distributed application runtime. It simplifies microservice communication (service invocation, pub/sub) and provides building blocks.

- Open Policy Agent (OPA) + OPA Gatekeeper: Used to enforce policies on the Kubernetes cluster itself. I'd create a policy to block direct Service-1 to Service-2 communication via NetworkPolicy.

- KEDA: Event-driven autoscaler for Kubernetes. You can use it to scale a service based on the length of the Kafka queue.

- Kafka: The message broker for the async Pub/Sub pattern facilitated by Dapr.

- YugabyteDB: A PostgreSQL-compatible distributed SQL database. The microservices will use it for persistence.

- Two Sample Microservices: Simple services order-service and user-service to demonstrate the patterns.

# High-Level Architecture

This is a textual diagram to visualize the flow.<br><br>

<img width="1550" height="1062" alt="image" src="https://github.com/user-attachments/assets/8375b15a-75a1-4b0c-812d-c3b70fe19b7c" />

# Install Essential Tools in Your Shell

- `helm` to install complex applications and the `dapr` CLI to manage Dapr, and `minikube` for Kubernetes. <br><br>

For this project, I had to use these minikube specifications <br><br>
`benedictokafor@fyng-sys-bokafor ~ % minikube start --cpus=2 --memory=2200mb --disk-size=20g` <br>

<img width="923" height="329" alt="image" src="https://github.com/user-attachments/assets/447d237a-5425-4dbf-8eb8-0368364b77e6" /> <br>
- minikube container  image up and running.
<img width="2906" height="862" alt="image" src="https://github.com/user-attachments/assets/cdd467eb-9825-42c2-99d1-c67e35114f8a" />

### Install Dapr into Minikube Cluster
`dapr init -k`<br>

This command installs the Dapr control plane (dapr-sidecar-injector, dapr-operator, dapr-placement, dapr-sentry) into the dapr-system namespace within the minikube cluster.<br>

###### Verify the installation by running:

`kubectl get pods -n dapr-system` or `dapr status -k` <br>

<img width="966" height="311" alt="image" src="https://github.com/user-attachments/assets/992bb40a-8a34-4eb4-a89c-53235eea8eb1" />

### Install Kafka using Helm
I utilize the Bitnami Kafka chart because it is well-maintained and includes ZooKeeper.<br><br>

- Add the Bitnami Helm repository:<br>
`
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
`<br>
- Install Kafka into a dedicated namespace:<br>

`
kubectl create namespace kafka
helm install kafka bitnami/kafka -n kafka \
  --set replicas=1 \
  --set zookeeper.replicaCount=1
`<br>
The --set flags override defaults to create a lighter, single-node setup suitable for Minikube.

- Verify the Kafka installation:<br>
`
kubectl get pods -n kafka -w
`<br>
###### N:B: Wait for the 'kafka-0' and 'zookeeper-0' pods to show STATUS 'Running'










