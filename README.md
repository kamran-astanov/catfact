# CatFact API Application

This is a simple Flask-based web application that fetches random cat facts from the [CatFact API](https://catfact.ninja/fact) and provides a health check endpoint.

## Table of Contents
- [Project Overview](#project-overview)
- [Installation](#installation)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
  - [Kubernetes with Helm Setup](#kubernetes-with-helm-setup)
- [Testing the Application](#testing-the-application)
- [CI/CD with GitHub Actions](#cicd-with-github-actions)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project is a Flask-based API application that:
- Fetches a random cat fact from an external API (`https://catfact.ninja/fact`).
- Exposes two main endpoints: 
  - `/catfact`: Returns a random cat fact.
  - `/health`: Returns a health check to ensure the application is running.
  
The application is containerized with Docker and can also be deployed to Kubernetes using Helm.

## Installation

### Local Setup

**Clone the Repository**:

	 git clone https://github.com/kamran-astanov/catfact.git

	 cd catfact
**Install Dependencies**:

	 pip install -r requirements.txt
**Run the Application Locally**:

	 python myapp.py



### Docker Setup
**Build the Docker Image**:

	 docker build -t catfact-app .
 **Run the Docker Container**:

	 docker run -p 5000:5000 catfact-app


### Kubernetes with Helm Setup
Install Helm (if you haven't already): Follow the installation instructions for Helm.

Create a Kubernetes Cluster: You can use a local cluster like Minikube or Kind.

**Install the Application Using Helm**:

	 helm install catfact-api ./charts
**Verify the Deployment**: 

	 kubectl get pods

	 kubectl get svc

**Access the Application**: 

If using Minikube or Kind, you may need to use port forwarding to access the app:

	 kubectl port-forward svc/catfact-api 8080:8080


## Testing the Application

To test the application locally or in Docker, you can use curl or Postman to check the endpoints:

Health Check:

	 curl http://localhost:8080/catfact

Example Response:

	 { 
	   "fact": "Cats have five toes on their front paws, but only four toes on their back paws."
	 }

Get Random Cat Fact:

	 curl http://localhost:8080/health

Example Response:

	 {
	   "status": "OK"
	 }

## CI/CD with GitHub Actions

**PATH** for CI/CD Pipeline: .github/workflows/ci-cd.yaml

This project is configured with GitHub Actions to automatically test and deploy the application.

### Workflow Steps:

### Steps Explained:

**1. Checkout Code**

- name: Checkout Code
  uses: actions/checkout@v3
  
This step checks out the code from the GitHub repository to the runner, ensuring that all the required files are available.

**2. Write Kind Configuration**

- name: Write Kind Configuration
  run: |
    cat <<EOF > kind-config.yaml
    kind: Cluster
    apiVersion: kind.x-k8s.io/v1alpha4
    networking:
      disableDefaultCNI: false
    nodes:
      - role: control-plane
        extraPortMappings:
          - containerPort: 5000
            hostPort: 5000
            protocol: TCP
    EOF

Generates a custom configuration for the Kind cluster. The extraPortMappings map Kubernetes container ports to the host for testing purposes.


**3. Set up Kubernetes with Kind**

- name: Set up Kubernetes with Kind
  run: |
    kind delete cluster --name kind || true
    kind create cluster --name kind --config=kind-config.yaml

Creates a Kubernetes cluster using Kind with the specified configuration.


**4. Remove Taint from Control Plane**

- name: Remove Taint from Control Plane
  run: |
    kubectl taint nodes --all node.kubernetes.io/not-ready-

Removes default taints from the control-plane node, enabling it to schedule workloads.



**5. Wait for Node to be Ready**

- name: Wait for Node to be Ready
  run: |
    echo "Waiting for node to be in Ready state..."
    for i in {1..10}; do
      kubectl get nodes | grep -q ' Ready ' && break
      echo "Node not ready yet. Retrying in 10s..."
      sleep 10
    done
    kubectl get nodes

Ensures the Kubernetes node is in the Ready state before proceeding.


**6. Verify Kind Cluster**

- name: Verify Kind Cluster
  run: |
    kubectl cluster-info
    kubectl get nodes

Verifies the Kind cluster setup by checking cluster information and node readiness.


**7. Set Kubernetes Context**

- name: Set Kubernetes Context
  run: |
    kubectl config use-context kind-kind

Sets the current Kubernetes context to the Kind cluster for subsequent commands.


**8. Install Helm****

- name: Install Helm
  uses: azure/setup-helm@v3

Installs Helm on the GitHub runner to manage Kubernetes deployments.








## Contributing

We welcome contributions! If you'd like to contribute to this project:

**Fork the repository**.

**Create a new branch** (git checkout -b feature-branch).

**Make your changes and commit them**.

**Push to the branch** (git push origin feature-branch).

## License

This project is licensed under the **MIT License**.
