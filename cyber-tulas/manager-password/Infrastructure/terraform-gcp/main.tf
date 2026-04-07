resource "google_compute_address" "my_ip" {
  name = "static-ip-address"
}


resource "google_compute_instance" "vm_instance" {
  name         = "terraform-vm"
  machine_type = var.machine_type
  zone         = "us-central1-a" 

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 20
    }
  }

  network_interface {
    network = "default"
    access_config {
      nat_ip = google_compute_address.my_ip.address
    }
  }

  # THE BRIDGE: This script runs automatically on the VM at startup
  metadata_startup_script = <<-EOT
    #!/bin/bash
    # Update system and install Docker + Docker Compose
    apt-get update
    apt-get install -y docker.io docker-compose
    
    # Enable Docker to start on boot
    systemctl enable docker
    systemctl start docker

    # Optional: Logic to pull  code/images would go here
    # Example: git clone https://github.com/your-repo /home/ubuntu/app
  EOT

  metadata = {
    ssh-keys = "ansible:${file("~/.ssh/id_ed25519.pub")}"
  }
}

resource "google_compute_firewall" "allow_access" {
  name    = "allow-ssh-http-app"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22", "80", "443", "8080"] 
  }

  source_ranges = ["0.0.0.0/0"] 
}