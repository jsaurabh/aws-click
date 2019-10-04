A collection of scripts written in Python3 for automating common AWS tasks. 

## Pre-Requisites
1. Python3
2. AWS Python SDK
   
   If you don't have the SDK installed, you can follow the instructions below:
        
        pip3 install boto3
3. AWS CLI
   
   Instructions on how to do so can be referred [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
   
   If you're on Windows, go ahead and download the Windows installer. I faced issues with getting the pip install to work.
    
## Usage

### One Time Setup
First, setup your AWS CLI. In a terminal window, type in 'aws configure' and follow the instructions on screen. You'll need your AWS Secure Secret Access Key and Secure Key handy. For first time usage, you'll need to create an IAM User and enable programmatic access. 

Follow the instructions available here at the [documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html).

Remember to save your credentials as this is the only time you'll be able to access them in plain text. In a terminal window, type in 'aws configure' and enter in the secure key and access key. Next, choose a region. For consistency, use us-east-1 as the default region.

    aws configure
    Access Key ID: your access key ID
    Secret Access Key: your secret key
    Default region: us-east-1
    Default output format: json

If you've never created an AWS keypair before, go ahead and create one now, with your chosen name:
    
    python keypair.py --create [name]

Great! Now, go on and create a new security group. Security groups define the inbound and traffic rules for any AWS resource, acting as a firewall. Just run the file 'instance-networking.py' and you're good to go. Refer to --help if you need instructions on usage.

Detailed instructions on how to launch, use and modify AWS resources can be found in the Docs


