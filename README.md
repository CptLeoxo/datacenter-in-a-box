# Datacenter in a box - Local DevOps Infrastructure 📦

A fully automated, locally deployed microservice infrastructure using Terraform and Docker. This project demonstrates industry-standard DevOps practices: Infrastructure as Code (IaC), secure secrets management, and Continuous Integration (CI).

## 🏗  Architecture & Tech Stack

The project consists of an isolated virtual Docker network (`datacenter_net`) running three containers:

*   **Reverse Proxy (Nginx):** Single entry point. Routes incoming HTTP requests securely to the internal backend.
*   **Backend (Python + Flask):** A REST API application running on a lightweight `python:3.11-slim` image.
*   **Database (PostgreSQL 15):** Relational database with an attached independent Docker Volume (`pg_data`) for persistent data storage.

**DevOps Tools:**
*   **Orchestration & Provisioning:** Terraform, Docker
*   **CI/CD:** GitHub Actions
*   **Testing:** Pytest (integrated into multi-stage Docker builds)

## ✨ Key Features

*   **Infrastructure as Code (IaC):** The entire network, images, volumes, and containers are declaratively defined in `main.tf`. Deploy and destroy the entire stack with a single command.
*   **Multi-stage Docker Builds:** The application build is split into `tester` and `runner` stages. Unit tests run automatically during the build process, blocking deployment if they fail.
*   **DevSecOps (Secrets Management):** Database credentials are never committed to version control. Terraform injects them via a local `.auto.tfvars` file which is strictly ignored by Git.
*   **Continuous Integration (CI):** On every push to the `main` branch, a GitHub Actions pipeline automatically validates Terraform syntax and verifies the Docker build integrity.

## 🚀 How to Run

### 1. Prerequisites
Ensure you have the following installed on your local machine (or WSL2):
*   Docker (with Docker Engine running)
*   Terraform
*   Git

### 2. Setup Secrets
Clone the repository and create a file for your local secrets (it is already protected by `.gitignore`):

```bash
git clone [https://github.com/CptLeoxo/datacenter-in-a-box.git](https://github.com/CptLeoxo/datacenter-in-a-box.git)
cd datacenter-in-a-box/terraform
touch secrets.auto.tfvars
```

Add your database credentials to `secrets.auto.tfvars`:
```hcl
db_user     = "admin"
db_password = "YourSecurePassword123!"
```

### 3. Deploy Infrastructure
Inside the `terraform` directory, initialize the providers and apply the configuration:

```bash
# Download required Docker providers
terraform init

# Preview changes
terraform plan

# Deploy the infrastructure (type 'yes' to confirm)
terraform apply
```

### 4. Verify Microservices
Once deployed, the infrastructure will be available at `http://localhost`. Test the endpoints in this order:

1.  `GET http://localhost/setup` — Initializes the database and creates the visitor table.
2.  `GET http://localhost/visit` — Records your current IP address and timestamp in PostgreSQL.
3.  `GET http://localhost/visitors` — Fetches the latest visit history from the database in JSON format.

## 🧹 Teardown

To stop the project and completely remove all associated containers, networks, and images, run:
```bash
terraform destroy
```
*(Note: The Docker Volume containing the database records will also be permanently deleted).*
