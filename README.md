# CatFact API Application

This is a simple Flask-based web application that fetches random cat facts from the [CatFact API](https://catfact.ninja/fact) and provides a health check endpoint.

## Table of Contents
- [Project Overview](#project-overview)
- [Installation](#installation)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
  - [Kubernetes with Helm Setup](#kubernetes-with-helm-setup)
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


## CI/CD with GitHub Actions

**PATH** for CI/CD Pipeline: .github/workflows/ci-cd.yaml

This project is configured with GitHub Actions to automatically test and deploy the application.

### Workflow Steps:

### Steps Explained:

**Checkout Code**
  
This step checks out the code from the GitHub repository to the runner, ensuring that all the required files are available.

**Write Kind Configuration**

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


**Set up Kubernetes with Kind**

    kind delete cluster --name kind || true
    
    kind create cluster --name kind --config=kind-config.yaml

Creates a Kubernetes cluster using Kind with the specified configuration.


**Remove Taint from Control Plane**

    kubectl taint nodes --all node.kubernetes.io/not-ready-

Removes default taints from the control-plane node, enabling it to schedule workloads.


**Wait for Node to be Ready**

    echo "Waiting for node to be in Ready state..."
    for i in {1..10}; do
      kubectl get nodes | grep -q ' Ready ' && break
      echo "Node not ready yet. Retrying in 10s..."
      sleep 10
    done
    kubectl get nodes

Ensures the Kubernetes node is in the Ready state before proceeding.


**Verify Kind Cluster**

    kubectl cluster-info
    
    kubectl get nodes

Verifies the Kind cluster setup by checking cluster information and node readiness.


**Set Kubernetes Context**

    kubectl config use-context kind-kind

Sets the current Kubernetes context to the Kind cluster for subsequent commands.


**Install Helm**

Installs Helm on the GitHub runner to manage Kubernetes deployments.

**Build Docker Image**

    docker build -t catfact-api .

Builds the Docker image for the CatFact API application.

**Load Docker Image into Kind**

    kind load docker-image catfact-api --name kind

Loads the Docker image into the Kind cluster for local use, bypassing the need for a container registry.

**Deploy Application using Helm**

    helm upgrade --install catfact-api ./charts

**Wait for Pods to be Ready**

    kubectl get pods
    sleep 10
    kubectl get pods

**Install Curl**

    sudo apt-get install -y curl

Installs curl on the GitHub runner for testing the application endpoints.

**Test Endpoints**

    kubectl port-forward service/catfact-api 8080:8080 &
    sleep 10

    # Test /catfact endpoint
    echo "Testing /catfact endpoint..."
    curl -s http://localhost:8080/catfact

    # Test /health endpoint
    echo "Testing /health endpoint..."
    curl -s http://localhost:8080/health


## Contributing

We welcome contributions! If you'd like to contribute to this project:

**Fork the repository**.

**Create a new branch** (git checkout -b feature-branch).

**Make your changes and commit them**.

**Push to the branch** (git push origin feature-branch).

## License

This project is licensed under the **MIT License**.
