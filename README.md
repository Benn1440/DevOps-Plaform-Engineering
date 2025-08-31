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

