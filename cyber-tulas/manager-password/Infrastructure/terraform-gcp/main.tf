
resource "google_compute_instance" "vm_instance" {
  name         = "terraform-vm"
  machine_type = var.machine_type             

 
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


  metadata = {
  ssh-keys = "ansible:${file("~/.ssh/id_ed25519.pub")}"
   }
}


resource "google_compute_firewall" "allow_access" {
  name    = "allow-ssh-http"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22", "80", "443", "8080"] 
  }

  source_ranges = ["0.0.0.0/0"] 
}

