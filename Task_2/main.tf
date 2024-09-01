terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.0.1"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Region zones to use with subnets
data "google_compute_zones" "available" {
  region  = var.region
  project = var.project_id
}

# VPC
resource "google_compute_network" "cloudfresh-test" {
  name = "${var.name}-vpc"

  delete_default_routes_on_create = false # Leaving default routes
  auto_create_subnetworks         = false # Prohibiting automatic creation of the subnets

  routing_mode = "GLOBAL" # 
}

# Firewall rules
resource "google_compute_firewall" "ingress-ssh" {
  name      = "${var.name}-firewall-ssh"
  network   = google_compute_network.cloudfresh-test.id
  direction = "INGRESS"

  source_ranges = ["0.0.0.0/0"]

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  allow {
    protocol = "udp"
    ports    = ["22"]
  }

  allow {
    protocol = "sctp"
    ports    = ["22"]
  }

  target_tags = ["allow-ssh"]
}

resource "google_compute_firewall" "ingress-icmp" {
  name      = "${var.name}-firewall-icmp"
  network   = google_compute_network.cloudfresh-test.id
  direction = "INGRESS"

  source_ranges = ["0.0.0.0/0"]

  allow {
    protocol = "icmp"
  }

  target_tags = ["allow-icmp"]
}

# Subnets
resource "google_compute_subnetwork" "this" {
  count         = 2
  name          = "${var.name}-subnet${count.index}"
  ip_cidr_range = var.subnets_cidrs[count.index]

  network = google_compute_network.cloudfresh-test.id
}

# VMs
resource "google_compute_instance" "vms" {
  count        = 2
  name         = "${var.name}-vm${count.index}"
  tags         = ["allow-ssh", "allow-icmp"]
  zone         = data.google_compute_zones.available.names[count.index]
  machine_type = "e2-small"

  network_interface {
    network    = google_compute_network.cloudfresh-test.id
    subnetwork = google_compute_subnetwork.this[count.index].id
    access_config {
      # Ephemeral public IP
    }
  }

  boot_disk {
    initialize_params {
      image = "ubuntu-2004-focal-v20240829"
    }
  }
}