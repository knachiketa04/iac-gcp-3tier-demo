# 🏗️ Architecture & Infrastructure Details

## 🏗️ **Infrastructure Components**

### **🌐 Networking Layer**

- **Custom VPC**: Isolated network environment
- **Private Subnets**: 10.10.10.0/24 CIDR block
- **Cloud NAT**: Outbound internet for private instances
- **Firewall Rules**: HTTP (port 80) and health check access
- **Load Balancer**: Global HTTP(S) load balancer

### **⚙️ Compute Layer**

- **Instance Template**: Debian 12, e2-medium instances
- **Managed Instance Group**: Regional deployment, auto-healing
- **Auto-scaler**: 2-4 instances based on CPU utilization (60%)
- **Service Account**: Dedicated account with Cloud SQL permissions

### **🗄️ Database Layer**

- **Cloud SQL**: PostgreSQL 14, db-g1-small tier
- **Security**: Cloud SQL Auth Proxy for secure connections
- **Schema**: Normalized tables (authors, quotes, user_votes)
- **Data**: Pre-populated with 7 authors and 11 inspirational quotes

### **🔀 Load Balancing**

- **HTTP Load Balancer**: Global, external facing
- **Health Checks**: HTTP endpoint monitoring
- **Backend Service**: Session affinity enabled
- **Auto-failover**: Unhealthy instance removal

## 🗄️ **Database Schema**

```sql
-- Authors table
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quotes table
CREATE TABLE quotes (
    id SERIAL PRIMARY KEY,
    author_id INTEGER REFERENCES authors(id),
    text TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'wisdom',
    upvotes INTEGER DEFAULT 0,
    downvotes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User votes table
CREATE TABLE user_votes (
    id SERIAL PRIMARY KEY,
    quote_id INTEGER REFERENCES quotes(id),
    user_ip VARCHAR(45),
    vote_type VARCHAR(10) CHECK (vote_type IN ('up', 'down')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(quote_id, user_ip)
);
```

**Sample Data Includes:**

- **Authors**: Albert Einstein, Maya Angelou, Steve Jobs, Nelson Mandela, Marie Curie, Mark Twain, Oprah Winfrey
- **Categories**: wisdom, success, attitude, innovation, perseverance, education, knowledge, motivation, dreams

## 🔒 **Security Features**

- ✅ **Network Isolation**: Private VPC with no public IPs on VMs
- ✅ **Database Security**: Cloud SQL Auth Proxy, private connections
- ✅ **IAM Best Practices**: Least privilege service accounts
- ✅ **Firewall Protection**: Restrictive rules, health check sources only
- ✅ **Secrets Management**: Database passwords via Terraform variables

## 📈 **High Availability & Scalability**

- ✅ **Auto-scaling**: Horizontal scaling based on CPU utilization
- ✅ **Load Balancing**: Traffic distribution across healthy instances
- ✅ **Health Monitoring**: Automatic instance replacement on failure
- ✅ **Regional Deployment**: Multi-zone instance distribution
- ✅ **Session Persistence**: Cookie-based session affinity
- ✅ **Database Reliability**: Managed Cloud SQL with automatic backups

## 🎯 **Important Outputs**

After deployment, Terraform provides these key outputs:

| Output                     | Description                     | Usage                         |
| -------------------------- | ------------------------------- | ----------------------------- |
| `load_balancer_ip`         | External IP of your application | Visit this IP in your browser |
| `database_connection_name` | Cloud SQL connection string     | For direct database access    |
| `vpc_network_name`         | VPC network name                | For network troubleshooting   |

## 🎨 **Customization Options**

### **Scaling Configuration**

```terraform
# In compute.tf, adjust auto-scaling
autoscaling_policy {
  min_replicas = 2      # Minimum instances
  max_replicas = 10     # Maximum instances (increase for higher load)
  cpu_utilization {
    target = 0.60       # Scale trigger (60% CPU)
  }
}
```

### **Database Tier Upgrade**

```terraform
# In cloud_sql.tf, upgrade instance
settings {
  tier = "db-n1-standard-1"  # More powerful database
}
```

### **Add New Quotes**

Add quotes by modifying the `init_database()` function in `app/app.py` or through the database directly.
