# Part 2 - Networking
In this part of the technical task I created infrastructure in the GCP that consists of:
1. VPC
2. Two subnets
3. Two VMs

All infrastructure was created using [Terraform]() and [gcloud]() cli.

Final network after completeing the task looked like this(visualised using GCP Network Topology tool):
![network topology](/Task_2//images/final%20network.png)

My process of creating needed infrastructure went like this:

### 1. Creating project and VPC

For starters I created three files: `main.tf`, `variables.tf` and `deployment.tfvars`. In `main.tf` I declared terraform configurations and requirements and google provider that uses variables from `variables.tf` to initialize connection to GCP.

To create VPC in google cloud platform, I used `google_compute_network` resource and created simple VPC with default routes and no subnets. I had no problems with this step and immediatly went to create subnets.

### 2. Creating subnets

To create subnets I used `google_compute_subnetwork` resource and declared createion of 2 subnets using `count` variable. After that I used `subnets_cidrs` variable to assign CIDRs for each of the subnets and assigned them to created VPC.
On this stage I encountered problem when creating subnets in for of the next error:
![terraform error](/Task_2/images/terraform%20error.png) 

After little of troubleshooting I understood that I used wrong name for the region("eu-central2" and not "europe-central2"). After changing value of the `region` variable all subnets were successfully created.
![successfull network creation](/Task_2/images/success%20creating%20network.png)

### 3. Creating VMs

Following successfull creating of subnets I started declaring `google_compute_instance` resource to create needed VMs. I followed [this](https://github.com/terraform-google-modules/terraform-docs-samples/blob/main/compute/basic_vm/main.tf) official tutorial to create VMs and modified it a little to create several of them from the start using `count` variable.

Virtual machines were successfully created:
![vms creation](/Task_2/images/vms%20creation.png)

But I encountered new problem. I couldn't connect to VMs using gcloud command:
```bash
gcloud compute ssh --zone "europe-central2-a" "cloudfresh-testing-vm0" --tunnel-through-iap --project "cloudfresh-test"
```
Resulting error told me that I forgot to add firewall rules to the VPC. After this I went back to `main.tf` and added firewall rules `ingress-ssh` and `ingress-icmp` that allow ingress ssh connection and icmp checks for VMs.

Finaly, after adding firewall rules I was successfull in connecting through `gcloud compute ssh` to VMs:
1. vm0:
    ![connection to vm0](/Task_2/images/connection%20to%20vm0.png)
2. vm1:
    ![connection to vm1](/Task_2/images/connection%20to%20vm1.png)
I also was successfull in pinging each VMs using internal IPs:
![ping test](/Task_2/images/ping%20test.png)