# Create a new VPC network for the application to ensure network isolation.
resource "google_compute_network" "vpc_network" {
  name                    = "${var.app_name}-vpc"
  auto_create_subnetworks = false
}

# Create a subnet within the VPC.
resource "google_compute_subnetwork" "app_subnet" {
  name                     = "${var.app_name}-subnet"
  ip_cidr_range            = "10.10.10.0/24"
  network                  = google_compute_network.vpc_network.id
  region                   = var.region
  private_ip_google_access = true  # Enable private Google access for Cloud SQL
}

# Firewall rule to allow HTTP traffic.
resource "google_compute_firewall" "allow_http" {
  name    = "${var.app_name}-fw-allow-http"
  network = google_compute_network.vpc_network.name
  allow {
    protocol = "tcp"
    ports    = ["80"]
  }
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["http-server"]
}

# Firewall rule to allow health checks from the Google Cloud Load Balancer.
resource "google_compute_firewall" "allow_health_check" {
  name    = "${var.app_name}-fw-allow-health-check"
  network = google_compute_network.vpc_network.name
  allow {
    protocol = "tcp"
    ports    = ["80"]
  }
  source_ranges = ["130.211.0.0/22", "35.191.0.0/16"]
  target_tags   = ["http-server"]
}

# A Cloud Router is required for Cloud NAT.
resource "google_compute_router" "router" {
  name    = "${var.app_name}-router"
  network = google_compute_network.vpc_network.id
  region  = google_compute_subnetwork.app_subnet.region
}

# Setup Cloud NAT to allow instances without public IPs to access the internet.
resource "google_compute_router_nat" "nat" {
  name                               = "${var.app_name}-nat-gateway"
  router                             = google_compute_router.router.name
  region                             = google_compute_router.router.region
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
  nat_ip_allocate_option             = "AUTO_ONLY"
  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}
