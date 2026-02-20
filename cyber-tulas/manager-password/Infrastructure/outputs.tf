output "ip_address" {
  value = google_compute_instance.vm_instance.network_interface.0.network_ip
}

output "instance_name" {
  value = google_compute_instance.vm_instance.name
}

output "instance_id" {
  value = google_compute_instance.vm_instance.instance_id
}

output "zone" {
  value = google_compute_instance.vm_instance.zone
}