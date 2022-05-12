# Final Project - User Guide

# Preliminaries
```
1. Set up VPC on AWS
https://docs.aws.amazon.com/vpc/index.html

2. Set up EC2 instance
https://aws.amazon.com/pm/ec2/

3. Set up Cloudwatch
https://aws.amazon.com/cloudwatch/

4. Set up S3 Bucket
https://aws.amazon.com/pm/serv-s3/

5. Set up AWS Cli on your local machine
https://aws.amazon.com/cli/

6. Copy webserver folder to your EC2 instance and run it
cd webserver
python3 app.py
```

# How to run the system
```
Running order is critical, users have to follow the running order below:

1. analyse service:
cd analyse_service
python3 app.py

2. msg filter service:
cd msg_filter_service
python3 app.py

3.dispatch service:
cd dispatch_service
python3 main.py

4. rule service:
cd rule_service
python3 main.py

5. initial attacks
cd local_tools
python3 port_scanner.py

# FYI
During implementing the code, if you are prompted missing packages, just use pip to install them. It will work.
```