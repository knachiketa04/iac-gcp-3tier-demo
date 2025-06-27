# 📂 Project Structure & File Organization

## **Directory Structure**

```
3-tier-application/
├── 🏗️ Infrastructure (Terraform)
│   ├── provider.tf              # GCP provider & backend config
│   ├── variables.tf             # Input variables definition
│   ├── terraform.tfvars.example # Configuration template
│   ├── network.tf              # VPC, subnets, firewall, NAT
│   ├── compute.tf              # VMs, auto-scaling, service accounts
│   ├── cloud_sql.tf            # PostgreSQL database setup
│   ├── load-balancer.tf        # HTTP load balancer configuration
│   └── outputs.tf              # Important resource outputs
├── 🎨 Application Code
│   ├── app/app.py              # Flask web application
│   ├── app/requirements.txt    # Python dependencies
│   ├── app/test_db.py          # Database connectivity test
│   └── app/templates/          # HTML templates
│       ├── base.html           # Common layout & styling
│       ├── index.html          # Quote of the Day page
│       ├── browse.html         # Browse quotes page
│       └── authors.html        # Authors page
├── 🚀 Deployment Scripts
│   ├── scripts/startup.sh      # VM startup script
│   └── scripts/README.md       # Script documentation
└── 📖 Documentation
    ├── README.md               # Main project overview
    ├── docs/ARCHITECTURE.md    # Infrastructure details
    ├── docs/TESTING.md         # Testing & validation guide
    ├── docs/TROUBLESHOOTING.md # Common issues & solutions
    └── DEPLOYMENT_SEQUENCE.md  # Detailed deployment flow
```

## **Key Files Explained**

### **Infrastructure Files**

- **`provider.tf`**: Configures GCP provider and Terraform backend
- **`variables.tf`**: Defines all input variables with validation
- **`network.tf`**: Creates VPC, subnets, firewall rules, and NAT gateway
- **`compute.tf`**: Manages VMs, auto-scaling, and service accounts
- **`cloud_sql.tf`**: Sets up PostgreSQL database with security
- **`load-balancer.tf`**: Configures HTTP load balancer and health checks
- **`outputs.tf`**: Exports important resource information

### **Application Files**

- **`app.py`**: Main Flask application with 3-tier architecture
- **`requirements.txt`**: Python dependencies (Flask, psycopg2, etc.)
- **`test_db.py`**: Database connectivity test script
- **`templates/`**: HTML templates with responsive design

### **Deployment Files**

- **`startup.sh`**: VM initialization script (refactored from compute.tf)
- **`terraform.tfvars.example`**: Example configuration file

### **Documentation Files**

- **`README.md`**: Quick start guide and overview
- **`ARCHITECTURE.md`**: Detailed infrastructure documentation
- **`TESTING.md`**: Testing procedures and API documentation
- **`TROUBLESHOOTING.md`**: Common issues and solutions
- **`DEPLOYMENT_SEQUENCE.md`**: Step-by-step deployment process

## **Why This Structure Works**

1. **Clear Separation**: Infrastructure, application, and documentation are well-separated
2. **Scalable**: Easy to add new components or modify existing ones
3. **Maintainable**: Each file has a single responsibility
4. **GitHub-Ready**: Follows best practices for open source projects
5. **Educational**: Clear organization helps users understand the architecture
