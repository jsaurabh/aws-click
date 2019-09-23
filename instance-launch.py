import click
import boto3 as b3
from botocore.exceptions import ClientError

ec2 = b3.resource('ec2')

AMI = {
    "GPU":{
        "Windows": {
            "AMI" : 'ami-0845b2806f525f91d' 
        },
        "Linux" : {
            "AMI" : 'ami-0845b2806f525f91d'
        }
    },
    "CPU":{
        "Windows": {
            "AMI" : 'ami-0845b2806f525f91d'
        },
        "Linux": {
            "AMI" : 'ami-0845b2806f525f91d'
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

def worker(instance, keypair):
    """
    Provision and launch an EC2 instance
    The method returns without waiting for the instance to reach
    a running state.

    :param instance: tuple, containing the AMI image_id and the instance type
    :param keypair: string, name of the key pair
    :returns Instance ID. If error, returns None.
    """
    
    try:
        assert len(instance) == 2, "Please enter only two arguments"
        assert keypair is not None, "Please enter a keypair to use with the instance"

    except ClientError as e:
        print("Refer to --help for usage")
        return None

    if instance:
        compute, platform = instance
        print("Compute chosen:" + compute)
        print("Platform chosen: " + platform)
        print("Enter custom config. Leave blank for default values")
        print("")
         
        instance_type = input("Enter the instance type:")
        if not instance_type:
            instance_type = 'g3s.xlarge'
        
        storage = input("Enter an integer value as the amount of storage (in GB)")
        if storage:
            storage = int(storage)
        if not storage:
            storage = 100

        ami = input("If you've got a pre-defined AMI, please enter the ID here.")
        if not ami:
            ami = AMI[compute][platform]
        
        # terminate = input("Disable programmatic instance termination:")
        # if not terminate:
        #     terminate = True
        # else:
        #     terminate = bool(terminate)

        try:
            instance = ec2.create_instances(
                BlockDeviceMappings = [
                    {
                        "DeviceName":"/dev/xvda",
                        "Ebs":{
                            "DeleteOnTermination" : False,
                            "VolumeSize" : storage
                            },
                    },   
                ],
                ImageId = ami['AMI'],
                InstanceType = instance_type,
                KeyName = keypair,
                MinCount = 1,
                MaxCount = 1,
                Monitoring =
                {
                    "Enabled": True
                },
                DryRun = True,
                DisableApiTermination = True,
                InstanceInitiatedShutdownBehavior = "stop"
            )

        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise
        
        try:
            instance = ec2.create_instances(
                BlockDeviceMappings = [
                    {
                        "DeviceName":"/dev/xvda",
                        "Ebs":{
                            "DeleteOnTermination" : False,
                            "VolumeSize" : storage
                            },
                    },   
                ],
                ImageId = ami['AMI'],
                InstanceType = instance_type,
                KeyName = keypair,
                MinCount = 1,
                MaxCount = 1,
                Monitoring =
                {
                    "Enabled": True
                },
                DryRun = False,
                DisableApiTermination = True,
                InstanceInitiatedShutdownBehavior = "stop"
            )

        except ClientError as e:
            print("Please check your config")
            print(e)
            return None
        
        print("Your instance has been created successfully! Refer to the console window for details")
        print(instance[0])
        return instance


if __name__ == "__main__":
    worker()

