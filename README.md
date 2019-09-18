A collection of scripts written in Python3 for automating common AWS tasks. You can create, start and stop instances, modify subnets, attach storage volumes and such using these scripts. 


## Pre-Requisites

    1. Python3
    2. AWS Python SDK
        If you don't have the SDK installed, you can follow the instructions below:
            pip3 install boto3

    3. AWS CLI
        Instructions on how to do so can be referred [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
    
## Usage
    The first thing to do is to configure your AWS account using the CLI you just installed in the previous step
    
    In a terminal window, type in 'aws configure' and follow the instructions on screen. You'll need your AWS Secure Secret Access Key and Secure Key handy. Detailed instructions are available at the [documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

    Once the cli configuration is done, go ahead and set up AWS keypairs as follows:
        python3 keypair.py --help