import click
import boto3 as b3
from botocore.exceptions import ClientError

ec2 = b3.client('ec2')

AMI = {
    "GPU":{
        "Windows": {
            "AMI" : 'ami-0845b2806f525f91d', #Windows
            "Type": 't2.micro' ## Replace with g3s.xlarge for GPU accelerated instances
        },
        "Linux" : {
            "AMI" : 'ami-0845b2806f525f91d',
            "Type": 't2.micro' ## Need to study appropriate instance type for CPU instances
        }
    },
    "CPU":{
        "Windows": {
            "AMI" : 'ami-0845b2806f525f91d',
            "Type": 't2.micro'
        },
        "Linux": {
            "AMI" : 'ami-0845b2806f525f91d',
            "Type": 't2.micro'
        }
    }
}

@click.command()
@click.option(
    "--instance", "--t", type=click.Choice(['GPU', 'CPU', 'Windows', 'Linux']), multiple = True,
    help = "Select type of instance to create. Options include GPU(accelerated compute),\
CPU for long running processes on both Windows and Linux")

@click.option(
    "--keypair", "--k",
    help = "Enter the keypair file name to use to access the new instance.\
If no keypair exists, create a new one using keypair.py")

def worker(instance, keypair):

    """Provision and launch an EC2 instance
    The method returns without waiting for the instance to reach
    a running state.

    :param instance: tuple, containing the AMI image_id and the instance type to use
    :param keypair: string, name of the key pair
    :return Instance ID. If error, returns None.
    """

    try:
        assert len(instance) == 2
        assert keypair is not None
    except ClientError as e:
        print("Please enter max 2 config params for instances. Make sure \
you've defined a keypair to use. Refer --help for possible values and usage")
        return None

    if instance:
        compute, platform = instance
        ami = AMI[compute][platform]
        image_id, instance_type = ami['AMI'], ami['Type']

        try:
            response = ec2.run_instances(ImageId = image_id,
                                 InstanceType = instance_type,
                                 KeyName = keypair,
                                 MinCount = 1,
                                 MaxCount = 1,
                                 Monitoring={'Enabled': True},
                                 DryRun=True
                                 )
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise
        
        try:
            response = ec2.run_instances(ImageId = image_id,
                                 InstanceType = instance_type,
                                 KeyName = keypair,
                                 MinCount = 1,
                                 MaxCount = 1,
                                 Monitoring={'Enabled': True},
                                 DryRun=False
                                 )
            print(response['Instances'][0]['ImageId'])
            print(response['Instances'][0]['InstanceId'])
        except ClientError as e:
            print("You do not have sufficient permissions or access to resources requested")
            print(e)
            return None
        
        return response['Instances'][0]['ImageId']


if __name__ == "__main__":
    worker()

