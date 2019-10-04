import click
import boto3 as b3
from botocore.exceptions import ClientError

ec2 = b3.client('ec2')
vpcs = ec2.describe_vpcs()
vpcID = vpcs.get('Vpcs', [{}])[0].get('VpcId', '')


@click.command()
@click.option(
    "--describe", "--d", 
    help = "View security groups associated with account. Enter the id as an argument")

@click.option(
    "--create", "-c", 
    help = "Add a new security group to the VPC. Pass name as an argument. Creates necessary ingress permissions as well."
)

@click.option(
    "--delete", "-d",
    help = "Delete existing security group."
)

def worker(describe, create, delete):

    if describe:
        try:
            response = ec2.describe_security_groups(
                GroupdIds=describe
            )
        except ClientError as e:
            print(e)

    elif create:
        try:
            response = ec2.create_security_group(GroupName=create,
                                                 Description="VNC Security group",
                                                VpcId=vpcID)

            security_group_id = response["GroupId"]
            print("Security Group Created {0} in vpc {1}".format(security_group_id, vpcID))

            data = ec2.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                    'FromPort': 8080,
                    'ToPort':8080,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                    'FromPort': 5900,
                    'ToPort':5900,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                    'FromPort': 3389,
                    'ToPort':3389,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                ])
                
            print("Ingress Set: {0}".format(data))
        except ClientError as e:
            print(e)
    elif delete:
        try:
            response = ec2.delete_security_group(GroupId='SECURITY_GROUP_ID')
            print("Security group has been deleted")
        except ClientError as e:
            print(e)
    else:
        print("Please enter an argument. Refer to --help for usage")

if __name__ == "__main__":
    worker()