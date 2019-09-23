import click
import boto3 as b3
from botocore.exceptions import ClientError

ec2 = b3.client('ec2')

@click.command()
@click.option(
    "--action","--a",
    help = "Start, stop, reboot or terminate an instance. Refer to --help for usage"
)

@click.argument('id')

def worker(action, id):
    if action.lower() == "on":
        print("You are starting an instance")
        try:
            response = ec2.start_instances(InstanceIds=[id], DryRun = True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print("Please make sure that you have the necessary permissions.")
                raise        
        
        try:
            response = ec2.start_instances(InstanceIds=[id])
            print(response)
            print("Instance started!")
        except ClientError as e:
            print("Error. Please make sure the instance ID is valid and belongs to you..")
    
    elif action.lower() == "off":
        print("You are stopping an instance")
        try:
            ec2.stop_instances(InstanceIds=[id], DryRun = True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print("Check completed.")
                raise        
        
        try:
            response = ec2.stop_instances(InstanceIds=[id])
            print(response)
            print("Instance stopped!")
        except ClientError as e:
            print("Error. Please make sure the instance ID is valid and belongs to you.")

    elif action.lower() == "reboot":
        print("You are rebooting an instance")
        try:
            ec2.reboot_instances(InstanceIds=[id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print("You don't have permission to reboot instances.")
                raise

        try:
            response = ec2.reboot_instances(InstanceIds=[id])
            print(response)
            print("Instance rebooted.")
        except ClientError as e:
            print("Error. Please make sure the instance ID is valid and belongs to you.")
        
    elif action.lower() == "terminate":
        print("You are terminating an instance")
        try:
            ec2.terminate_instances(InstanceIds=[id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print("Error. Please make sure the instance ID is valid and belongs to you.")
                raise

        try:
            response = ec2.terminate_instances(InstanceIds=[id], DryRun=False)
            print(response)
            print("Instance terminated.")
        except ClientError as e:
            print("You don't have permission to terminate instances. Set disableApiTermination to False to terminate an instance programatically.")
        
    else:
        print("Please enter a valid action. Available actions include start, stop or terminate instance")

if __name__ == "__main__":
    worker()