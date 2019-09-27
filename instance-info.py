from collections import defaultdict
import click
import boto3 as b3
from botocore.exceptions import ClientError, ParamValidationError
from utils import set_info

ec2 = b3.resource('ec2')
info = defaultdict()

choices = ['running', 'stopped', 'terminated']

@click.command()
@click.option(
    "--state", type=click.Choice(choices),
    help = "Enter the state you want to query instances on. \
Available choices include running, stopped and terminated.") 

def worker(state):
    try:
        filters = ec2.instances.filter(
            Filters=[{
                'Name': 'instance-state-name',
                'Values': [state]}])
    
        #TODO Change to accomodate when multiple tags are set
        #Hacky soln but works for now.
        for instance in filters:
            if instance.tags:
                for tag in instance.tags:
                    if 'Name' in tag['Key']:
                        name = tag['Value']
                    else:
                        name = ''
            else:
                name = ''
            
            info[instance.id] = {
                'ID': instance.id,
                'Name': name,
                'Type': instance.instance_type,
                'State': instance.state['Name'],
                'Public IP': instance.public_ip_address,
                'Private IP': instance.private_ip_address
            }

    except ClientError as e:
        print(e) 
    except ParamValidationError as e:
        print("Please enter arguments and values")

    for _, instance in info.items():
        set_info(instance)

if __name__ == "__main__":
    worker()