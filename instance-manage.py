import click
import boto3 as b3
from botocore.exceptions import ClientError
from config import Config

ec2 = b3.client('ec2')

@click.command()
@click.option(
    "--monitor", "--m", type = click.Choice(['on', 'off']),
    help = "Enable or disable CloudWatch monitoring for your instance. \
    Go to https://console.aws.amazon.com/cloudwatch for more details")

@click.option("--describe", "--d", is_flag = True,
    help = "Describe the instance")

def worker(monitor, describe):
    instance = input("Choose an instance tag name to act upon(config.ini):")
    id = Config.get_from_section(instance, 'id')

    if describe:
        try:
            response = ec2.describe_instances(InstanceIds=[id])
            print("Describing instance id: " + id)
            print(response)
        
        except ClientError as e:
            print(e)

    else:
        if monitor == "on":
            print("Switching to Detailed Monitoring")
            response = ec2.monitor_instances(InstanceIds=[id])
            print(response)
        else:
            print("Switching to Basic Monitoring")
            response = ec2.unmonitor_instances(InstanceIds=[id])
            print(response)

if __name__ == "__main__":
    worker()