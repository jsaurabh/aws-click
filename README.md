A collection of scripts written in Python3 for automating common AWS tasks. 

## Pre-Requisites
1. Python3
2. AWS Python SDK
    If you don't have the SDK installed, you can follow the instructions below:
        pip3 install boto3
3. AWS CLI
    Instructions on how to do so can be referred [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
    
## Usage

### One Time Setup
First, setup your AWS cli. In a terminal window, type in 'aws configure' and follow the instructions on screen. You'll need your AWS Secure Secret Access Key and Secure Key handy. For first time usage, you'll need to create an IAM User and enable programmatic access. 

Follow the instructions available here at the [documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html).
    NOTE: Choose the EC2FullAccessPolicy rather than AdministratorAccess to ensure consistency across accounts.

Remember to save your credentials as this is the only time you'll be able to access them in plain text. In a terminal window, type in 'aws configure' and enter in the secure key and access key. Next, choose a region. 
    NOTE: For consistency, use us-east-1a as the default region.

If you've never created an AWS keypair before, go ahead and create one now, with your chosen name:
    python keypair.py --create [name]

Great! The initial config is all done. You can go ahead and start checking out resources.

## EC2 Instances
