terraform {
  required_version = ">= 1.8.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.65.0"
    }
  }
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

# Network for instance
# VPC
module "flask-vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.13.0"

  name = "flask-vpc"
  cidr = "10.0.0.0/16"

  azs            = var.azs
  public_subnets = [for k, v in var.azs : cidrsubnet("10.0.0.0/16", 8, k + 10)]

  map_public_ip_on_launch = true

  enable_nat_gateway = false

  default_route_table_routes = [
    {
      cidr_block = "0.0.0.0/0"
      gateway_id = module.flask-vpc.igw_id
    }
  ]
}
# Security groups
module "flask-sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "5.2.0"

  name        = "flask-sg"
  description = "Security group for simple Flask app"
  vpc_id      = module.flask-vpc.vpc_id

  # Allowing HTTP/HTTPS, ICMP and SSH for everyone
  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["http-80-tcp", "https-443-tcp", "all-icmp", "ssh-tcp"]

  # Allowing egress to everywhere
  egress_cidr_blocks = ["0.0.0.0/0"]
  egress_rules       = ["all-all"]
}

# Creating key for EC2 vm
resource "aws_key_pair" "flask-vm-key" {
  key_name   = "flask-key"
  public_key = var.public_key
}

# Fetching ubuntu image for VM
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["amazon"]
}

# Creating needed VM
module "flask-vm" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "5.7.0"

  name = "flask-dev"

  instance_type          = "t2.micro"
  ami                    = data.aws_ami.ubuntu.id
  key_name               = aws_key_pair.flask-vm-key.key_name
  monitoring             = false
  vpc_security_group_ids = [module.flask-sg.security_group_id]
  subnet_id              = module.flask-vpc.public_subnets[0]
}