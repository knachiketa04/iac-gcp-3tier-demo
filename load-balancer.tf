# Health check to monitor the application instances and determine which are
# healthy instances. These settings are made more lenient to give the application time to start.
resource "google_compute_health_check" "http_health_check" {
  name                = "app-http-health-check"
  check_interval_sec  = 15
  timeout_sec         = 10
  healthy_threshold   = 2
  unhealthy_threshold = 3

  http_health_check {
    port         = 80
    request_path = "/api/health"  # Use dedicated health endpoint
  }
}

# Backend service defines how the load balancer distributes traffic.
resource "google_compute_backend_service" "app_backend" {
  name                  = "${var.app_name}-infra-lb-backend-default"
  protocol              = "HTTP"
  port_name             = "http"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  timeout_sec           = 30
  health_checks         = [google_compute_health_check.http_health_check.id]
  session_affinity      = "GENERATED_COOKIE"

  backend {
    group = google_compute_region_instance_group_manager.app_mig.instance_group
  }
}

# URL map to route all incoming requests to our backend service.
resource "google_compute_url_map" "default_map" {
  name            = "${var.app_name}-lb-url-map"
  default_service = google_compute_backend_service.app_backend.id
}

# The HTTP proxy that uses the URL map.
resource "google_compute_target_http_proxy" "http_proxy" {
  name    = "${var.app_name}-http-proxy"
  url_map = google_compute_url_map.default_map.id
}

# The global forwarding rule, which gives us a public IP address.
resource "google_compute_global_forwarding_rule" "forwarding_rule" {
  name                  = "${var.app_name}-infra-lb"
  target                = google_compute_target_http_proxy.http_proxy.id
  port_range            = "80"
  load_balancing_scheme = "EXTERNAL_MANAGED"
}
