# financial_data_pipelines_with_docker
##Introduction
This project was made in order to gain very basic familiarity with the Airflow orchestration tool, and the AWS RDS database resource.
Yahoo Finance FX and Equity Index data for different batch times is extracted using the yfinance Python library.  The data is converted to the parquet format and stored in an s3 bucket.

An Airflow dag senses when the separate FX and Equity Index parquet files arrive in the s3 bucket, and triggers functions to write the data to separate tables in the RDS instance.  Airflow will then only write a data-batch-complete flag to a third table once both the corresponding FX and Equity Index data for the batch has been fully inserted.

##Setup
###Python
```
pip install -r requirements. txt
```

###Airflow and Docker
Setup Airflow following the pattern established in the following webpage, including adding connection to the postgres database in the web UI:
https://airflow.apache.org/docs/apache-airflow/stable/tutorial/pipeline.html

Then run the following to get it up and running:
```
docker compose up 
```

In order to place the necessary functions into the Docker container so that Airflow can use them, and also allow AWS access, the relevant filepaths had to be added to docker-compose.yaml under _PIP_ADDITIONAL_REQUIREMENTS: 
```
    - ~/.aws/:/home/airflow/.aws
    - ${AIRFLOW_PROJ_DIR:-.}/src/yfinance_fx_transform_and_load:/opt/airflow/plugins/src/yfinance_fx_transform_and_load
    - ${AIRFLOW_PROJ_DIR:-.}/src/yfinance_equity_index_transform_and_load:/opt/airflow/plugins/src/yfinance_equity_index_transform_and_load
    - ${AIRFLOW_PROJ_DIR:-.}/src/utilities:/opt/airflow/plugins/src/utilities
    - ${AIRFLOW_PROJ_DIR:-.}/src/yfinance_batch_completion:/opt/airflow/plugins/src/yfinance_batch_completion
```

Additionally the project's requirements.txt file had to be cut down and stored as airflow_requirements.txt file, in order to avoid Airflow webserver issues, and included in a separate Dockerfile which builds the Airflow image and is referenced in the docker-compose.yaml file by
```
 "build: .". 
```
The Docker image using these Airflow requirements can then be built using
```
docker-compose build
```

###terraform
Create an s3 bucket which will be used to store the terraform state file.

For example, in the AWS CLI:
```
aws s3 mb s3://yfinance-ingest-backend
```
Then make sure that the backend "s3" bucket name, inside the terraform provider.tf file, is changed to match your newly-created bucket's name:
```terraform
provider "aws" {
  region  = "eu-west-2"
}

terraform {
  backend "s3" {
    bucket = "yfinance-ingest-backend"
    key    = "application.tfstate"
    region = "eu-west-2"
  }
}
```

Within the .terraform folder (within the terraform folder) the vars.tfvars file should contain your choice of credentials to connect to the RDS instance:
```terraform
db_credentials = {
    "db_credentials": {
        "port": "your_required_port",
        "dbname": "your_database_name",
        "engine": "postgresql",	
        "username": "your_username",
        "password": "your_password"
    }
}
```
These values are used to create an AWS Secret, within secrets.tf

This file will then be read during terraform apply and plan by explicitly referencing it, e.g.,
```
terraform apply -var-file=".terraform/vars.tfvars"
```
Note that the "host" required to connect to the db is not present in .tfvars.  This was added manually to the Secret created by Terraform from within the AWS Management Console (see below).


###AWS Management Console
The RDS "host" value was added manually to the Secret created by Terraform from within the AWS Management Console, using the endpoint of the RDS instance observed in the AWS Management Console as its value.
The RDS security group also had to be changed to allow ingress into the RDS port from my personal public IP address.
Also altered pg_hba.conf and postgresql.conf files in /etc/postgresql/14/main, to include rule for my personal public IP address and to listen on all addresses, respectively. 


###PostgreSQL
Local pg_hba.conf and postgresql.conf files within
``` 
/etc/postgresql/14/main
```
had to be altered, to include a rule for my personal public IP address and to listen on all addresses, respectively.
