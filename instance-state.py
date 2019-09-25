import click
import boto3 as b3
from botocore.exceptions import ClientError
from config import Config
error = "Error. Please make sure the instance ID is valid and belongs to you."
ec2 = b3.client('ec2')

@click.command()
@click.option(
    "--action","--a",
    help = "Start, stop, reboot or terminate an instance. Arguments include on, off, reboot and terminate for respective effect."
)

@click.option(
    "--dry", is_flag = True,
    help = "Set whether to do a dry run or not. A dry run will check for necessary permissions without executing the command."
)

def worker(action, dry):
    instance = input("Choose an instance name to act upon(config.ini):")
    instance_id = Config.get_from_section('current', instance)

    if action.lower() == "on":
        print("You are starting an instance")
        try:
            response = ec2.start_instances(InstanceIds=[instance_id], DryRun = dry)
            print(response)
            print("Instance started.")
            print("Please remember to turn off your instance when you're done.")
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print("Please make sure that you have the necessary permissions.")
                raise 
            print(error)
        
    elif action.lower() == "off":
        print("You are stopping an instance")
        try:
            response = ec2.stop_instances(InstanceIds=[instance_id], DryRun = dry)
            print(response)
            print("Instance stopped.")
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print("Check completed.")
                raise        
            print(error)

    elif action.lower() == "reboot":
        print("You are rebooting an instance")
        try:
            response = ec2.reboot_instances(InstanceIds=[instance_id], DryRun = dry)
            print(response)
            print("Instance rebooted.")
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print("You don't have permission to reboot instances.")
                raise
            print(error)
        
    elif action.lower() == "terminate":
        print("You are terminating an instance")
        try:
            response = ec2.terminate_instances(InstanceIds=[instance_id], DryRun = dry)
            print(response)
            print("Instance terminated.")
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print(error)
                raise
            print("You don't have permission to terminate instances. Change Termination Protection policy to terminate the instance programatically.")
        
    else:
        print("Please enter a valid action. Available actions include start, stop, reboot or terminate instance")

if __name__ == "__main__":
    worker()