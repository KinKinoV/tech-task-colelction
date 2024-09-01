output "instance_pub_ip" {
  value = module.flask-vm.public_ip
}

output "instance_dns" {
  value = module.flask-vm.public_dns
}