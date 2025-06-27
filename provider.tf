# Configure the Terraform backend to use Google Cloud Storage.
# The state file will be named "default.tfstate" and stored at the root of the bucket.
# You must provide the bucket name via:
# 1. Backend config file: terraform init -backend-config="bucket=your-bucket-name"
# 2. Or uncomment and update the bucket name below
terraform {
  backend "gcs" {
    # bucket = "your-terraform-state-bucket" # Uncomment and update with your bucket name
  }
}

# Configure the Google Provider.
provider "google" {
  project = var.project_id
  region  = var.region
}