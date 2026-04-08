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

    mkdir -p /home/ansible/cyber-tulas
    cd /home/ansible/cyber-tulas
    # Клонуємо, якщо папка порожня
    git clone https://github.com/T1maty/cyber-tulas.git .
  EOT

  metadata = {
    ssh-keys = "ansible:ssh-ed25519 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPj27X2WcE7A/LYygexD1Rpzpk90R0rhqBHxP35fSNyz tomas@fedora"
  }
}