# 🏗️ 3-Tier Web Application on Google Cloud Platform

[![Terraform](https://img.shields.io/badge/Terraform-1.0+-623CE4)](https://terraform.io)
[![GCP](https://img.shields.io/badge/GCP-Supported-4285f4)](https://cloud.google.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **Production-ready 3-tier web application deployed on Google Cloud Platform using Terraform**

## 🎯 **What This Is**

A complete **"Quote of the Day"** platform demonstrating:

- **🎨 Presentation Tier**: Interactive web interface with voting system
- **⚙️ Application Tier**: Flask REST API with business logic
- **🗄️ Data Tier**: PostgreSQL database with normalized schema

**Features**: Browse quotes, vote on favorites, explore authors, real-time rankings

## 🏗️ **Architecture**

```
🌐 Internet → 🔀 Load Balancer → ⚙️ Flask VMs → 🗄️ PostgreSQL
```

- **Auto-scaling**: 2-4 instances based on CPU utilization
- **High Availability**: Multi-zone deployment with health checks
- **Security**: Private VPC, Cloud SQL Auth Proxy, IAM best practices

## 🚀 **Quick Start**

### **Prerequisites**

- GCP account with billing enabled
- `gcloud` CLI authenticated
- Terraform installed (v1.0+)

### **1. Configure**

```bash
# Clone and configure
git clone <your-repo>
cd 3-tier-application
cp terraform.tfvars.example terraform.tfvars

# Edit with your details
nano terraform.tfvars
```

**Required variables:**

```hcl
project_id       = "your-gcp-project-id"
app_name        = "webapp-example"          # Must start with lowercase letter
gcs_bucket_name = "your-terraform-bucket"   # For state storage
db_password     = "your-secure-password"
```

### **2. Deploy**

```bash
terraform init
terraform plan
terraform apply  # Takes ~10-15 minutes
```

### **3. Access**

```bash
# Get your application URL
terraform output load_balancer_ip

# Visit: http://[LOAD_BALANCER_IP]
```

## 🎯 **What You Get**

- **Interactive Web App**: Vote on quotes, browse by category
- **REST API**: `/api/quote-of-the-day`, `/api/quotes`, `/api/authors`
- **Auto-scaling Infrastructure**: Handles traffic spikes automatically
- **Production Security**: Private networks, managed database, IAM roles

## � **Documentation**

| Guide                                              | Description                                 |
| -------------------------------------------------- | ------------------------------------------- |
| [Architecture Details](docs/ARCHITECTURE.md)       | Infrastructure components & database schema |
| [Testing Guide](docs/TESTING.md)                   | API endpoints, load testing, monitoring     |
| [Troubleshooting](docs/TROUBLESHOOTING.md)         | Common issues & solutions                   |
| [Deployment Sequence](docs/DEPLOYMENT_SEQUENCE.md) | Step-by-step deployment process             |

## 🔧 **Common Issues**

### **Naming Errors**

```
Error: "account_id" must match regex...
```

**Fix**: Ensure `app_name` starts with lowercase letter (e.g., `webapp-example`)

### **Permissions**

Ensure your GCP account has: `Compute Admin`, `SQL Admin`, `Security Admin`

## 🧹 **Cleanup**

```bash
terraform destroy  # Removes all resources
```

## 💰 **Cost**

**~$50-80/month** for development environment:

- 2x e2-medium VMs (~$30)
- Cloud SQL instance (~$15)
- Load balancer (~$18)
- Network costs (~$5-15)

## 🎓 **Learning Value**

Perfect for understanding:

- ✅ Infrastructure as Code with Terraform
- ✅ 3-tier architecture patterns
- ✅ GCP services integration
- ✅ Auto-scaling and load balancing
- ✅ Security best practices

## 🤝 **Contributing**

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 **License**

MIT License - see [LICENSE](LICENSE) for details.

---

**🚀 Ready to deploy? Start with the Quick Start guide above!**
