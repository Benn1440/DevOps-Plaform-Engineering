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
`<br>
`helm repo update`
<br><br>
<img width="736" height="111" alt="image" src="https://github.com/user-attachments/assets/5627ee52-c86e-476a-a2af-2e4b2daf9ad1" />

- Install Kafka into a dedicated namespace:<br>
`
kubectl create namespace kafka 
`<br><br>
`helm install kafka bitnami/kafka -n kafka \
  --set replicas=1 \
  --set zookeeper.replicaCount=1`<br>
The --set flags override defaults to create a lighter, single-node setup suitable for Minikube.<br><br>
<img width="1118" height="268" alt="image" src="https://github.com/user-attachments/assets/6d349872-a2e1-46cf-8bb7-7fbc9b7ed837" /><br>

- Verify the Kafka installation:<br>
`
kubectl get pods -n kafka -w
`<br>
###### N:B: Wait for the 'kafka-0' and 'zookeeper-0' pods to show STATUS 'Running'
<img width="724" height="243" alt="image" src="https://github.com/user-attachments/assets/3be08967-ba30-4a82-8352-245a7c65297b" /><br><br>

## Next Step is to Install YugabyteDB using Helm
Add the YugabyteDB Helm repository:
`helm repo add yugabytedb https://charts.yugabyte.com`<br>

`helm repo update`<br>
- Install YugabyteDB into a dedicated namespace:<br>

`kubectl create namespace yugabyte`<br><br>
`helm install yb-demo yugabytedb/yugabyte -n yugabyte \
  --set replicas.master=1 \
  --set replicas.tserver=1 \
  --set resource.master.requests.memory=1Gi \
  --set resource.master.requests.cpu=0.5 \
  --set resource.tserver.requests.memory=1Gi \
  --set resource.tserver.requests.cpu=0.5`<br><br>

<img width="946" height="379" alt="image" src="https://github.com/user-attachments/assets/920c48b3-676d-40a3-8ef0-11c83d53b0ad" />

This configuration is for a minimal local deployment.

- Verify the YugabyteDB installation:<br>

`kubectl get pods -n yugabyte -w`<br>
###### N:B: Wait for the master and tserver pods to be in Running state. as it can take a few minutes.<br><br>
<img width="557" height="141" alt="image" src="https://github.com/user-attachments/assets/44dbf146-6aeb-4147-bf3e-1e736b103836" /><br><br>

## Next Step is to Install Apache APISIX using Helm

- Add the APISIX Helm repository:

`helm repo add apisix https://charts.apiseven.com`<br>
`helm repo update`<br>

- Install APISIX into a dedicated namespace:

`kubectl create namespace apisix`<br><br>
`helm install apisix apisix/apisix -n apisix \
  --set gateway.type=NodePort \
  --set gateway.http.nodePort=30000 \
  --set admin.allow.ipList="{0.0.0.0/0}"`<br><br>
This configures the APISIX gateway to be accessible on http://<minikube-ip>:30000.

- Verify APISIX installation:<br><br>
`kubectl get pods -n apisix`<br><br>
<img width="1065" height="412" alt="image" src="https://github.com/user-attachments/assets/39124713-b0b9-452a-808d-9c70f6bc0a8d" /><br><br>
<img width="789" height="311" alt="image" src="https://github.com/user-attachments/assets/b7828d7d-bf55-4bbe-82b5-aa234a210e4a" /><br><br>

## Next Step is to Install OPA Gatekeeper
OPA Gatekeeper is the admission controller we'll use to enforce our network policy.

- Install Gatekeeper:<br>

`kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml`<br><br>
###### This installs it into the gatekeeper-system namespace.

- Verify the OPA Gatekeeper installation:<br>

`kubectl get pods -n gatekeeper-system` <br><br>
<img width="1378" height="753" alt="image" src="https://github.com/user-attachments/assets/4ed70f73-e162-4449-8af0-7bc0c7bdc718" /> <br><br>
<img width="794" height="106" alt="image" src="https://github.com/user-attachments/assets/4d9921bc-5fad-4bf8-b26a-1fcdc419b1d7" /> <br><br>










