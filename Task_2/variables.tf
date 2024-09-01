variable "project_id" {
  description = "ID of the GCP project"
  type        = string
}

variable "region" {
  description = "Region name to use with deployment"
  type        = string
  default     = "europe-central2"
}

variable "name" {
  description = "Common name for all infrastruction components"
  type        = string
}

variable "subnets_cidrs" {
  description = "List of CIDRs to use when creating subnets"
  type        = list(string)
  default     = ["10.10.10.0/24", "10.10.20.0/24"]
}