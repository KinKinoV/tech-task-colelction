variable "azs" {
  description = "List of availability zones that VPC will cover"
  type        = list(string)
}

variable "public_key" {
  description = "Public part of the SSH key to use with deployed EC2 instance"
  type        = string
  sensitive   = true
}