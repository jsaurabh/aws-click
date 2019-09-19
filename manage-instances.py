import click
import boto3 as b3
from botocore.exceptions import ClientError

ec2 = b3.client('ec2')
@click.command()
@click.option(
    "--action","--a",
    help = "Start, stop, reboot or terminate an instance. \
OptionNeeds Instance ID. Refer to /docs/ for help and usage"
)

@click.argument('id')

def worker(action, id):
    if action.lower() == "on":
        print("You are starting an instance")
        try:
            ec2.start_instances(InstanceIds=[id], DryRun = True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print("Check completed.")
                raise        
        
        try:
            response = ec2.start_instances(InstanceIds=[id], DryRun = False)
            print(response)
            print("Instance started!")
        except ClientError as e:
            print("Error. Please try again. Refer to /docs for help and usage")
    
    elif action.lower() == "off":
        print("You are stopping an instance")
        try:
            ec2.stop_instances(InstanceIds=[id], DryRun = True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print("Check completed.")
                raise        
        
        try:
            response = ec2.stop_instances(InstanceIds=[id], DryRun = False)
            print(response)
            print("Instance stopped!")
        except ClientError as e:
            print("Error. Please try again. Refer to /docs for help and usage")

    # elif action.lower() == "reboot":
    #     print("You are rebooting an instance")
    #     try:
    #         ec2.reboot_instances(InstanceIds=[id], DryRun=True)
    #     except ClientError as e:
    #         if 'DryRunOperation' not in str(e):
    #             print("You don't have permission to reboot instances.")
    #             raise

    #     try:
    #         response = ec2.reboot_instances(InstanceIds=[id], DryRun=False)
    #         print('Success', response)
    #     except ClientError as e:
    #         print('Error', e)
        
    elif action.lower() == "terminate":
        print("You are trying to terminate an instance")
        try:
            ec2.terminate_instances(InstanceIds=[id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print("You don't have permission to reboot instances.")
                raise

        try:
            response = ec2.terminate_instances(InstanceIds=[id], DryRun=False)
            print('Success', response)
        except ClientError as e:
            print("Error")
            print(e)
        
    else:
        print("Please enter a valid action. Available actions include start, stop, reboot or terminate instance")

if __name__ == "__main__":
    worker()