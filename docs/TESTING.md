# 🧪 Testing & Validation Guide

## 📱 **Application Features**

### **🏠 Home Page - Quote of the Day**

- Random daily quote display
- Interactive voting system (👍👎)
- Real-time vote counts
- Author biography snippets
- Auto-refresh every 30 seconds

### **📚 Browse Page - Quote Library**

- Complete quote collection
- Category filtering (wisdom, success, motivation, etc.)
- Sort by popularity (vote score)
- Pagination support

### **✍️ Authors Page - Meet the Minds**

- Author profiles with biographies
- Quote count statistics
- Author rankings

### **🔌 REST API Endpoints**

- `GET /api/quote-of-the-day` - Random quote
- `GET /api/quotes` - All quotes with optional category filter
- `GET /api/authors` - Author list with statistics
- `POST /api/vote` - Submit vote for a quote
- `GET /api/health` - Health check for load balancer

## 🧪 **Testing Your 3-Tier Architecture**

### **1. Verify Each Tier**

```bash
# Test Presentation Tier (Load Balancer)
curl -I http://[LOAD_BALANCER_IP]

# Test Application Tier (REST API)
curl http://[LOAD_BALANCER_IP]/api/quote-of-the-day
curl http://[LOAD_BALANCER_IP]/api/quotes?category=wisdom
curl http://[LOAD_BALANCER_IP]/api/health

# Test Data Tier (via API)
curl -X POST http://[LOAD_BALANCER_IP]/api/vote \
  -H "Content-Type: application/json" \
  -d '{"quote_id": 1, "vote_type": "up"}'
```

### **2. Load Testing**

```bash
# Basic load test with Apache Bench
ab -n 1000 -c 10 http://[LOAD_BALANCER_IP]/

# Test auto-scaling trigger
ab -n 5000 -c 50 http://[LOAD_BALANCER_IP]/api/quote-of-the-day
```

### **3. Monitoring & Debugging**

```bash
# Check VM logs
gcloud compute ssh [INSTANCE_NAME] --zone=[ZONE] --command="sudo journalctl -u quote-app.service -f"

# Monitor startup process
gcloud compute ssh [INSTANCE_NAME] --zone=[ZONE] --command="sudo tail -f /var/log/startup.log"

# Test database connectivity
gcloud compute ssh [INSTANCE_NAME] --zone=[ZONE] --command="cd /opt/quote-app && python3 test_db.py"
```
