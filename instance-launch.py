import click
import boto3 as b3
from botocore.exceptions import ClientError, WaiterError
from utils import set_info

ec2R = b3.resource('ec2')
ec2C = b3.client('ec2')

AMI = {
    "GPU":{
        "Windows": {
            "AMI" : '' 
        },
        "Linux" : {
            "AMI" : ''
        }
    },
    "CPU":{
        "Windows": {
            "AMI" : ''
        },
        "Linux": {
            "AMI" : ''
        }
    }
}

@click.command()
@click.option(
    "--instance", "--i", type=click.Choice(['GPU', 'CPU', 'Windows', 'Linux']), multiple = True,
    help = "Select type of instance to create. Options include GPU and CPU for Windows and Linux.\
        Attach --instance flag for each choice")

@click.option(
    "--keypair", "--k",
    help = "Enter the keypair file name to use to access the new instance.\
If no keypair exists, create a new one using keypair.py")

@click.option(
    "--dry", is_flag = True,
    help = "Set to True to test if you have permission to launch instances.\
To create the instance, remove --dry flag from input."
)

def worker(instance, keypair, dry):
    """
    Provision and launch an EC2 instance
    The method returns after waiting for the instance to reach
    a running state.

    :param instance: tuple, containing the AMI image_id and the instance type
    :param keypair: string, name of the key pair
    :returns Instance ID. If error, returns None.
    """
    
    assert len(instance) == 2, "Please enter two arguments for --i"
    assert keypair is not None, "Please enter a keypair to use with the instance"

    if instance:
        compute, platform = instance
        print("Compute chosen:" + compute)
        print("Platform chosen: " + platform)
        print("Enter custom config. Leave blank for default values")
        print("")
         
        instance_type = input("Enter instance type (default g3s.xlarge):")
        if not instance_type:
            instance_type = 'g3s.xlarge'
        
        storage = input("Enter an integer value as the amount of storage (default 300 GB):")
        if storage:
            storage = int(storage)
        if not storage:
            storage = 300

        ami = input("Enter AMI image ID if you have one:")
        if not ami:
            ami = AMI[compute][platform]

        count = input("Enter the integer value of number of instances you want to create(default 1):")
        if count:
            count = int(count)
        if not count:
            count = 1
        
        tag = input("Enter a tag to associate with the instance: ")
        while not tag:
            tag = input("Enter a tag to associate with the instance: ")

        sg_id = input("Enter security group ID: ")
        while not sg_id:
            sg_id = input("Please enter a security group: ")
        try:
            instances = ec2R.create_instances(
                BlockDeviceMappings = [
                    {
                        "DeviceName":"/dev/sda1",
                        "Ebs":{
                            "DeleteOnTermination" : True,
                            "VolumeSize" : storage
                            },
                    },   
                ],
                ImageId = ami['AMI'],
                InstanceType = instance_type,
                KeyName = keypair,
                MinCount = 1,
                MaxCount = count,
                # SecurityGroupIds = [sg_id],
                Monitoring = {"Enabled": False},
                DryRun = dry,
                DisableApiTermination = False,
                InstanceInitiatedShutdownBehavior = "stop"
            )

        except ClientError as e:
            print(e)
            return None
     
        for instance in instances:
            try:
                print("Please wait while the instance is up and running")
                instance.wait_until_running()
                print("\n")
                print("Instance id: " + str(instances[0]))
                elasticIP = ec2C.allocate_address(Domain = 'vpc', DryRun = dry)
                print("Static IP address has been allocated: " + str(elasticIP['PublicIp']))

                ec2C.associate_address( 
                    InstanceId = instance.id,
                    DryRun = dry,
                    AllocationId = elasticIP["AllocationId"])

            except WaiterError as e:
                print(e)
                print("Please make sure any AWS resource limits have not been reached")

        print("\nYour instance has been launched and configured successfully.\
Instructions on using VNC can be found under docs")
        return None

if __name__ == "__main__":
    worker()