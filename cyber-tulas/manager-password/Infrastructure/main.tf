
provider "google" {
  project = "cyber-tulas" 
  region  = "us-central1"                
  zone    = "us-central1-a"
}


resource "google_compute_instance" "vm_instance" {
  name         = "terraform-vm"
  machine_type = "e2-micro"              

 
  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
      size  = 20
    }
  }


  network_interface {
    network = "default"
    access_config {
      
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


output "ip_address" {
  value = google_compute_instance.vm_instance.network_interface.0.access_config.0.nat_ip
}