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

	 curl http://localhost:8080/health

Example Response:

	 { 
	   "fact": "Cats have five toes on their front paws, but only four toes on their back paws."
	 }

Get Random Cat Fact:

	 curl http://localhost:8080/catfact

Example Response:

	 {
	   "status": "healthy"
	 }

## CI/CD with GitHub Actions

This project is configured with GitHub Actions to automatically test and deploy the application.

### Workflow Steps:

**Build Docker Image**: The workflow builds the Docker image on every push to the main branch.

**Run Tests**: Tests are run using curl or a similar tool to verify the application is responding.

**Deploy to Kubernetes**: The workflow also deploys the app to a Kubernetes cluster using Helm.


### Check the Workflow:

The workflow runs automatically whenever you push code to GitHub.

You can see the status of the workflow in the Actions tab of the repository.

## Contributing

We welcome contributions! If you'd like to contribute to this project:

**Fork the repository**.

**Create a new branch** (git checkout -b feature-branch).

**Make your changes and commit them**.

**Push to the branch** (git push origin feature-branch).

## License

This project is licensed under the **MIT License**.
