# Variables for the 3-tier application infrastructure

variable "project_id" {
  description = "The GCP project ID where resources will be created"
  type        = string
  # No default value - must be provided by user for security
}

variable "region" {
  description = "The GCP region where resources will be deployed"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "app_name" {
  description = "Application name used for resource naming (must start with lowercase letter, contain only lowercase letters, numbers, and hyphens)"
  type        = string
  default     = "webapp-example"
  
  validation {
    condition     = can(regex("^[a-z]([a-z0-9-]*[a-z0-9])?$", var.app_name))
    error_message = "The app_name must start with a lowercase letter and contain only lowercase letters, numbers, and hyphens. It cannot start or end with a hyphen."
  }
}

variable "gcs_bucket_name" {
  description = "GCS bucket name for Terraform state storage (must be globally unique, lowercase letters, numbers, hyphens, and dots only)"
  type        = string
  # No default value - must be provided by user
  
  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9._-]*[a-z0-9]$", var.gcs_bucket_name)) && length(var.gcs_bucket_name) >= 3 && length(var.gcs_bucket_name) <= 63
    error_message = "The gcs_bucket_name must be 3-63 characters, start and end with lowercase letter or number, and contain only lowercase letters, numbers, hyphens, and dots."
  }
}

variable "db_user" {
  description = "Database username"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Database password - use a strong password"
  type        = string
  sensitive   = true
  # No default value - must be provided by user for security
}
