import click
import boto3 as b3
from botocore.exceptions import ClientError, ParamValidationError
from config import Config
from utils import update

ec2 = b3.client('ec2')
error = "Error. Please make sure the instance ID is valid and belongs to you"

@click.command()
@click.option(
    "--action","--a", type=click.Choice(['on', 'off', 'reboot', 'terminate']),
    help = "Start, stop, reboot or terminate an instance."
)

@click.option(
    "--dry", is_flag = True,
    help = "Set whether to do a dry run or not. A dry run will check for necessary permissions without executing the command."
)

def worker(action, dry):
    try:
        instance = input("Choose an instance tag to act upon(config.ini):")
        instance_id = Config.get_from_section(instance, 'id')

        if action.lower() == "on":
            print("You are starting an instance")
            try:
                response = ec2.start_instances(InstanceIds=[instance_id], DryRun = dry)
                print(response)
                update(instance, 'state', 'running')
                print("Please remember to turn off your instance when you're done.")
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    print(permission)
                    raise 
                print(error)
            
        elif action.lower() == "off":
            print("You are stopping an instance")
            try:
                response = ec2.stop_instances(InstanceIds=[instance_id], DryRun = dry)
                print(response)
                update(instance, 'state', 'stopped')
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    print(permission)
                    raise        
                print(error)

        elif action.lower() == "reboot":
            print("You are rebooting an instance")
            try:
                response = ec2.reboot_instances(InstanceIds=[instance_id], DryRun = dry)
                print(response)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    print(e)
                    raise
                print(error)
            
        elif action.lower() == "terminate":
            print("You are terminating an instance")
            try:
                response = ec2.terminate_instances(InstanceIds=[instance_id], DryRun = dry)
                print(response)
                update(instance, 'state', 'terminated')
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    print(error)
                    raise
            
        else:
            print("Please enter a valid action. Look at help for instructions")
    except ClientError as e:
        print(e)
    except ParamValidationError as e:
        print("Please enter arguments and values")

if __name__ == "__main__":
    worker()