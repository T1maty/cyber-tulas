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

  service_account {
    scopes = ["cloud-platform"]
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    apt-get update
    apt-get install -y docker.io docker-compose git

    systemctl enable docker
    systemctl start docker
    usermod -aG docker ansible

    mkdir -p /home/ansible/cyber-tulas
    rm -rf /home/ansible/cyber-tulas/*
    cd /home/ansible/cyber-tulas

  
    git clone https://github.com/T1maty/cyber-tulas.git .

    chown -R ansible:ansible /home/ansible/cyber-tulas

    cd /home/ansible/cyber-tulas/manager-password
    docker-compose -f docker-compose.prod.yml up --build  -d
  EOT

  metadata = {
    ssh-keys = "ansible:ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPj27X2WcE7A/LYygexD1Rpzpk90R0rhqBHxP35fSNyz tomas@fedora"
  }
}

resource "google_compute_firewall" "allow_access" {
  name    = "allow-ssh-http-app"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22", "80", "443", "8080"]
  }

  source_ranges = ["${var.admin_ip}/32"]
}

