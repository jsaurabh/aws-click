import click
import boto3 as b3
import shutil
from botocore.exceptions import ClientError
from pathlib import Path
from config import Config

ec2 = b3.client('ec2')

@click.command()
@click.option(
    "--create",
    help = "Enter name for new keypair. The public key will be pushed to AWS and the private key will be saved locally.")
        
@click.option(
    "--delete",
    help = "Enter name for keypair to delete. The public key will be deleted from AWS. "
)

## TODO: Add keypair describe. Moderate change to docstring, and definition
def worker(create, delete):
    """Create or delete EC2 Key Pairs

    The method doesn't return anything. Will update keypair values on EC2 console as per arguments.

    :param create: string, Name of new keypair to create. Will be saved locally as name.pem
    :param delete: string, Name of keypair to delete. Public key will be deleted from EC2 console.
    returns None.
    """

    if create:
        try:        
            keypair = ec2.create_key_pair(KeyName=create)
            print("Keypair was created successfully.")
            filename = create + ".pem"
            with open(filename, 'w') as key:
                key.write(keypair['KeyMaterial'])
            print("Keypair file has been saved locally under current working directory")
            print("Please move to ~/.ssh on your machine and make it unreadable")
            print(keypair)

        except ClientError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)

    if delete:
        try:
            keypair = ec2.delete_key_pair(KeyName=delete)
            print(delete + " has been deleted. Please set up a different keypair to access compute resources")
            
        except ClientError as e:
            print(e)
            
    if not delete and not create:
        click.echo("Please enter an argument and its value. Refer to --help for usage details.")

if __name__ == "__main__":
    worker()