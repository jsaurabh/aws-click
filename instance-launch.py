import click
import boto3 as b3
from botocore.exceptions import ClientError, WaiterError
from utils import set_instance, set_ip

ec2R = b3.resource('ec2')
ec2C = b3.client('ec2')

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

@click.option(
    "--dry", is_flag = True,
    help = "Set to True to test if you have permission to launch instances. Will \
        lead to DryRunOperation if permissions exist. To create the instance, remove --dry flag from input."
)

def worker(instance, keypair, dry):
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
        
        storage = input("Enter an integer value as the amount of storage (in GB):")
        if storage:
            storage = int(storage)
        if not storage:
            storage = 100

        ami = input("If you've got a pre-defined AMI, please enter the ID here:")
        if not ami:
            ami = AMI[compute][platform]

        # print("")
        # print("Enter Yes or No")
        # print("If you enter yes, the instance can't be terminated without modifying instance properties")
        # terminate = input("Disable instance termination:")
         
        # if not terminate:
        #     allowTerminate = True
        # elif terminate == "No":
        #     allowTerminate = False
        # else:
        #     allowTerminate = True
        
        try:
            instance = ec2R.create_instances(
                BlockDeviceMappings = [
                    {
                        "DeviceName":"/dev/xvda",
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
                MaxCount = 2,
                Monitoring =
                {
                    "Enabled": True
                },
                DryRun = dry,
                DisableApiTermination = False,
                #DisableApiTermination = allowTerminate
                InstanceInitiatedShutdownBehavior = "stop"
            )

        except ClientError as e:
            print(e)
            return None
        
        print("Your instance has been created successfully.")
     
        count = 0
        for instances in instance:
            count +=1
            try:
                set_instance(instances.id, count)
                #print("")
                print("Please wait while the instance is up and running")
                instances.wait_until_running()

                elasticIP = ec2C.allocate_address(Domain = 'vpc', DryRun = dry)
                print("Static IP address has been allocated: " + str(elasticIP['PublicIp']))
                set_ip(elasticIP['PublicIp'], count)

                ec2C.associate_address(
                    InstanceId = instances.id,
                    DryRun = dry,
                    AllocationId = elasticIP["AllocationId"]
                )
                print("")
            except WaiterError as e:
                print(e)
                print("Please make sure any AWS resource limits have not been reached")

        print("Instance(s) associated with Static IP")
        print("Go ahead and start using the instance with the static IP.\
For instructions on Remote Desktop on Windows, refer to RDP-Windows.md")
        return None
        #return instance[0], elasticIP['PublicIp']

if __name__ == "__main__":
    worker()