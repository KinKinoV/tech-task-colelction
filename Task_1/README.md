# Part 1 - DevOps and DevSecOps
In this part of the assesment I created simple Python web application using Flask and set up a CI/CD pipeline using GitHub Actions. Additionally implemented basic security measures. Original repository is available [here](https://github.com/KinKinoV/cloudfresh-test-task)

Before implementing CI/CD pipeline I also deployed simple infrastructure to AWS using Terraform that consists of VPC, Security Group and EC2 instance. Used Terraform code is located in the [/python_infra](/Task_1/python_infra/) folder. Documentation for it is in the same place.

## CI/CD
To implement CI/CD pipelines I used GitHub Actions that are doing next things:
1. CI:
    - Checks if it's possible to build Flask application in python 3.10
    - Tests if you are able to successfully install flaskExample pip package
    - Tests whole flask application using pytest and tests provided in `pyton_app/tests` folder
2. CD:
    - SSH into the set up development EC2 instance in AWS by using `AWS_PRIVATE_KEY`, `HOST_NAME` and `USER_NAME` actions environment secrets
    - Switches directory to one where flask application is located using `APP_DIR` actions environment secret
    - Pulls all new code from GitHub repository
    - Restarts gunicorn service that is responsible for flask application (name of the service is stored in `SERVICE_NAME` actions environment secret)
    - Tests if CD was successfull and nothing broke by fetching `/hello` page from the app on `SITE_DNS` address
CI/CD pipelines are triggering only on pushes and pull requests into the `main` branch. Additionally, set up instructions for the EC2 instance so that it will be able to serve flask application is described in [infrastructure's README.md](/Task_1/python_infra/README.md).

## Security
This task requires implementing basic security for the app. To achieve it I've implemnted next measures:
1. Environment variables:
    - Because Flask doesn't provide easy ways to use exactly `.env` file in project, I used `config.py` file that is needed for the same type of functionality. It is loaded by Flask application during startup if no test configuratioons were passed into the app constructor
2. HTTPS:
    - Secure connection was implemented using certbot. Specifics of what was done is described in [infrastructure's README.md](/Task_1/python_infra/README.md/#https)
3. SCA using Codacy
    - To perform static code analysis I used Codacy by connecting it to my GitHub account and enabling scans for this repository. You can see results of the code scan here:

![codacy dashboard](/Task_1/images/codacy_dashboard.png)
![codacy issues breakdown](/Task_1/images/issues_breakdown.png)
