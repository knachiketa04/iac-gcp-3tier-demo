# 🔧 Troubleshooting Guide

## **Common Issues & Solutions**

### **Naming Convention Errors**

```
Error: "account_id" must match regex "^[a-z]([-a-z0-9]*[a-z0-9])?$"
```

**Solution**: Ensure `app_name` starts with lowercase letter and contains only lowercase letters, numbers, and hyphens.

**Valid examples:**

- ✅ `webapp-example`
- ✅ `my-demo-app`
- ❌ `3-tier-app` (starts with number)
- ❌ `My_App` (uppercase and underscores)

### **Permission Errors**

```
Error: Error creating instance template: googleapi: Error 403: Required 'compute.instanceTemplates.create' permission
```

**Solution**: Ensure your GCP user/service account has the following roles:

- `Compute Admin`
- `SQL Admin`
- `Security Admin`
- `Service Account Admin`

### **Quota Exceeded**

```
Error: Quota 'CPUS' exceeded. Limit: 8.0 in region us-central1.
```

**Solution**: Request quota increase in GCP Console or choose a different region.

### **State Bucket Issues**

```
Error: Failed to get existing workspaces: querying Cloud Storage failed: storage: bucket doesn't exist
```

**Solution**: Create the GCS bucket first or comment out the backend configuration for local state.

### **Database Connection Issues**

```
Error: Failed to connect to database
```

**Solutions:**

1. Verify Cloud SQL instance is running
2. Check Cloud SQL Auth Proxy logs: `sudo journalctl -u cloud-sql-proxy.service`
3. Verify service account has Cloud SQL permissions
4. Check firewall rules allow health checks

### **Load Balancer 502 Errors**

**Solutions:**

1. Check if VMs are healthy: `gcloud compute backend-services get-health [BACKEND_SERVICE]`
2. Verify application is running on port 80
3. Check health check endpoint: `/api/health`
4. Review VM startup logs

## **Debugging Tips**

1. **Check Terraform logs**: `export TF_LOG=DEBUG`
2. **Validate configuration**: `terraform validate`
3. **Check GCP permissions**: `gcloud auth list`
4. **Review resource quotas**: GCP Console → IAM & Admin → Quotas
5. **Monitor VM startup**: `sudo tail -f /var/log/startup.log`
6. **Check application logs**: `sudo journalctl -u quote-app.service -f`

## **GCP Naming Conventions Reference**

| Resource Type       | Rules                                                                   | Example                 |
| ------------------- | ----------------------------------------------------------------------- | ----------------------- |
| **Service Account** | Start with lowercase letter, 6-30 chars, lowercase/numbers/hyphens only | `webapp-compute` ✅     |
| **VPC Network**     | Start with lowercase letter, 1-63 chars, lowercase/numbers/hyphens only | `webapp-vpc` ✅         |
| **GCS Bucket**      | Globally unique, 3-63 chars, lowercase/numbers/hyphens/dots             | `my-terraform-state` ✅ |

## **Cost Optimization**

### **Development Environment** (~$50-80/month):

- 2x e2-medium instances (~$30/month)
- db-g1-small Cloud SQL (~$15/month)
- Load balancer (~$18/month)
- Network egress (~$5-15/month)

### **Production Optimization Tips**:

- Use Preemptible instances for cost savings
- Consider committed use discounts
- Monitor and optimize database tier
- Set up budget alerts

## **Cleanup**

To destroy all resources and avoid charges:

```bash
# Destroy infrastructure
terraform destroy

# Clean up local files
rm -rf .terraform/
rm terraform.tfstate*
```
