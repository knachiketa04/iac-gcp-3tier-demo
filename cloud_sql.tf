# Create the Cloud SQL instance for PostgreSQL.
resource "google_sql_database_instance" "app_instance" {
  name             = "${var.app_name}-instance"
  database_version = "POSTGRES_14"
  region           = var.region

  # Disable deletion protection for easier cleanup
  deletion_protection = false

  settings {
    tier = "db-g1-small" # A cost-effective tier suitable for labs
    ip_configuration {
      # This enables a public IP. The Cloud SQL Auth Proxy will be used for secure connections.
      ipv4_enabled = true
    }
  }
}

# Create the specific database (schema) within the instance.
resource "google_sql_database" "app_db" {
  name     = "${var.app_name}-db"
  instance = google_sql_database_instance.app_instance.name
}

# Create the user for the application to connect with.
resource "google_sql_user" "postgres_user" {
  name     = var.db_user
  instance = google_sql_database_instance.app_instance.name
  password_wo = var.db_password  # Use write-only password for better security
}