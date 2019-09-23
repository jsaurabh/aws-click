import click
import boto3 as b3
from botocore.exceptions import ClientError

ec2 = b3.client('ec2')

@click.command()
@click.option(
    "--monitor", "--m", default = "ON",
    help = "Enable or disable CloudWatch monitoring for your instance. \
    Go to https://console.aws.amazon.com/cloudwatch for more details")

@click.option("--describe", "--d", is_flag = True,
    help = "Describe the instance")

@click.argument('id')

def instances(monitor, describe, id):
    if describe:
        try:
            response = ec2.describe_instances(InstanceIds=[id])
            print("Describing instance id: " + id)
            print(response)
        
        except ClientError as e:
            print("Please enter valid instance identifier")
            print(e)

    elif monitor:
        if monitor == "ON":
            print("Enabling Detailed Monitoring")
            response = ec2.monitor_instances(InstanceIds=[id])
            print(response)
        else:
            print("Switching to Basic Monitoring")
            response = ec2.unmonitor_instances(InstanceIds=[id])
            print(response)

if __name__ == "__main__":
    instances()