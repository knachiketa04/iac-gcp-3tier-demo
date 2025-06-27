# Service account for compute instances to access Cloud SQL
resource "google_service_account" "app_service_account" {
  account_id   = "${var.app_name}-compute"
  display_name = "Service Account for ${var.app_name} Compute Instances"
}

# IAM binding for Cloud SQL Client role
resource "google_project_iam_member" "cloudsql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.app_service_account.email}"
}

# IAM binding for Cloud SQL Instance User role
resource "google_project_iam_member" "cloudsql_instance_user" {
  project = var.project_id
  role    = "roles/cloudsql.instanceUser"
  member  = "serviceAccount:${google_service_account.app_service_account.email}"
}

# Instance template defines the blueprint for our application VMs.
resource "google_compute_instance_template" "app_template" {
  name_prefix  = "${var.app_name}-template-"
  machine_type = "e2-medium"
  tags         = ["http-server"]

  disk {
    source_image = "debian-cloud/debian-12"
    auto_delete  = true
    boot         = true
  }

  # Connect the instances to our custom subnet.
  # Note: The instances themselves won't have public IPs.
  network_interface {
    subnetwork = google_compute_subnetwork.app_subnet.id
  }

  # Reference the external startup script with variable substitution
  metadata_startup_script = templatefile("${path.module}/scripts/startup.sh", {
    APP_PY_CONTENT          = file("${path.module}/app/app.py")
    TEST_DB_CONTENT         = file("${path.module}/app/test_db.py")
    REQUIREMENTS_CONTENT    = file("${path.module}/app/requirements.txt")
    BASE_TEMPLATE_CONTENT   = file("${path.module}/app/templates/base.html")
    INDEX_TEMPLATE_CONTENT  = file("${path.module}/app/templates/index.html")
    BROWSE_TEMPLATE_CONTENT = file("${path.module}/app/templates/browse.html")
    AUTHORS_TEMPLATE_CONTENT = file("${path.module}/app/templates/authors.html")
    CONNECTION_NAME         = google_sql_database_instance.app_instance.connection_name
    DB_USER                = var.db_user
    DB_PASS                = var.db_password
    DB_NAME                = "${var.app_name}-db"
  })

  # Service account with permissions needed for the VM to access other Google Cloud services.
  service_account {
    email  = google_service_account.app_service_account.email
    scopes = ["cloud-platform"]
  }
}

# Regional Managed Instance Group (MIG) to manage our application VMs.
resource "google_compute_region_instance_group_manager" "app_mig" {
  name   = "${var.app_name}-infra-lb-group1-mig"
  region = var.region

  version {
    instance_template = google_compute_instance_template.app_template.id
  }

  # This block explicitly tells the load balancer which port to use for the "http" service.
  named_port {
    name = "http"
    port = 80
  }

  base_instance_name = "${var.app_name}-app-vm"
  target_size        = 2 # Start with 2 instances.
}

# Autoscaler policy for the MIG.
resource "google_compute_region_autoscaler" "app_autoscaler" {
  name   = "${var.app_name}-autoscaler"
  region = google_compute_region_instance_group_manager.app_mig.region
  target = google_compute_region_instance_group_manager.app_mig.id

  autoscaling_policy {
    min_replicas    = 2
    max_replicas    = 4
    cooldown_period = 60

    cpu_utilization {
      target = 0.60 # Scale up if average CPU usage is > 60%
    }
  }
}