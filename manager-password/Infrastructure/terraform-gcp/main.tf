resource "google_compute_firewall" "allow_access" {
  name    = "allow-ssh-http-app"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22", "80", "443", "8080"]
  }

  source_ranges = ["${var.admin_ip}/32"]

  lifecycle {
    create_before_destroy = true
  }
}