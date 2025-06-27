# Output values for the 3-tier application

output "load_balancer_ip" {
  description = "External IP address of the load balancer"
  value       = google_compute_global_forwarding_rule.forwarding_rule.ip_address
}

output "vpc_network_name" {
  description = "Name of the VPC network"
  value       = google_compute_network.vpc_network.name
}

output "vpc_network_id" {
  description = "ID of the VPC network"
  value       = google_compute_network.vpc_network.id
}

output "subnet_name" {
  description = "Name of the application subnet"
  value       = google_compute_subnetwork.app_subnet.name
}

output "database_connection_name" {
  description = "Cloud SQL instance connection name"
  value       = google_sql_database_instance.app_instance.connection_name
}

output "database_instance_name" {
  description = "Cloud SQL instance name"
  value       = google_sql_database_instance.app_instance.name
}

output "database_name" {
  description = "Database name"
  value       = google_sql_database.app_db.name
}

output "instance_group_manager_name" {
  description = "Name of the managed instance group"
  value       = google_compute_region_instance_group_manager.app_mig.name
}

output "project_id" {
  description = "GCP Project ID"
  value       = var.project_id
}

output "region" {
  description = "GCP Region"
  value       = var.region
}
