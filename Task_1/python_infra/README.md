# Infrastructure for flaskExample application
Infrastructure needed for this task was deployed to AWS using Terraform. Meaning, to deploy infrastructure you need to have [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) and [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) installed on your machine.

Terraform modules used and inputs needed for this project are listed [here](#modules-used-and-inputs).

## Infrastructure deployment and destruction

To deploy infrastructure follow this instruction:
1. Change directory to `/python_infra`
2. Create `.tfvars` file and define all needed inputs
3. Execute `terraform apply -var-file=your.tfvars`
4. Confirm that terraform will deploy all needed infrastructure and then confirm apply with `yes`
5. After terraform deploys infrastructure you should be able to ssh into the EC2 instance using `instance_dns` output

To destroy created infrastructure execute `terraform destroy -var-file=your.tfvars` in the `/python_infra` folder.

## VM set up
Before deploying flaskExample application to the EC2 instance you need to set up VM. Steps you need to follow are these:
1. SSH into the deployed EC2 instance using `instance_pub_ip` or `instance_dns` output.
2. Install `nginx`, `git`, `python3-venv` and python of at least version `3.10`.
3. Go to directory where you desire to deploy flaskExample app and then `git copy` this repository.
4. `cd` into the downloaded `cloudfresh-test-task` directory and execute next command:
```bash
python3 -m venv ./venv
```
5. After creating python virtual environment activate it (`source venv/bin/activate`) and install all dependencies by executing `pip install -r python_app/requirements.txt`.
6. Following successfull installation of python dependencies you should execute next commands:
```bash
cd python_app/
# Creating DB for the app
flask --app flaskExample init-db
# Creating env file with secret key for the app
echo "SECRET_KEY = '$(python -c 'import secrets; print(secrets.token_hex())')'" > instance/config.py
```
7. Now you can deactivate virtual environment. Next step is to create service for the flaskExample app. To do this you need:
    - Execute `sudo nano /etc/systemd/system/flaskExample.service`. This will create `.service` file and open it in editor.
    - Paste the code from [example.service](/Task_1/python_infra/example.service) file into yours while changing what is different for you
    - Execute these commands:
```bash
sudo systemctl start flaskExample
sudo systemctl enable flaskExample
sudo systemctl status flaskExample # to check if service is working properly
```
8. To configure nginx to proxy requests to gunicorn you have to create new config file in `/etc/nginx/sites-available/`:
    - Execute `sudo nano /etc/nginx/sites-available/flaskExample`
    - Copy contents of the [site_conf_example](/Task_1/python_infra/site_conf_example) to the newly created file and edit it to fit your deployment needs
    - Create a link from sites-available to sites-enabled folder: `sudo ln -s /etc/nginx/sites-available/flaskExample /etc/nginx/sites-enabled`
    - Restart nginx using this command: `sudo systemctl restart nginx`
9. Now you should be able to go to the domain name you entered on step 8 and see this homepage:
![flaskExample homepage](/Task_1/images/appHomePage.png)
If you get `502 Bad Gateway` error, it means Nginx cannot access gunicorn’s socket file. To fix this give `755` permisions to the folder where `cloudfresh-test-task` is located.

## HTTPS
To implement HTTPS for your site, just install `python3-certbot-nginx` and execute next command:
```bash
sudo certbot --nginx -d your.domain.name.com
```
After that certbot will ask you several questions and it will automatically reconfigure your flaskExample site to use issued SSL certificates. And now your site has secure connections:
![secure connection to the site](/Task_1/images/secureConnection.png)

## Modules used and Inputs
Modules:
| Name | Version |
|------|---------|
|[terraform-aws-modules/vpc/aws](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/5.13.0)|5.13.0|
|[terraform-aws-modules/security-group/aws](https://registry.terraform.io/modules/terraform-aws-modules/security-group/aws/5.2.0)|5.2.0|
|[terraform-aws-modules/ec2-instance/aws](https://registry.terraform.io/modules/terraform-aws-modules/autoscaling/aws/5.7.0)|5.7.0|

Inputs:
| Name | Description | Type | Module |
|------|-------------|------|--------|
| azs  | List of availability zones that VPC will cover | `list(string)` | flask-vpc |
| public_key | Public part of the SSH key to use with deployed EC2 instance | `string` | flask-vm |