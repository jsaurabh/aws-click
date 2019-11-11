# Launch a VM on AWS

Dependencies:
    1. Recommended VNC Client
        
        TightVNC for Windows
        Remmina for Ubuntu
    
    2. One time setup as outlined in README.md in the root dir

## Launch instance

To launch an instance, run the file 

    python instance-launch.py

which comes with good defaults for the purposed of this project. To look at the options available, run the above command with the --help flag. 

The available options include GPU and CPU instances for both Windows and Linux. 

To select a GPU Linux instance(Recommended), set the instance flags as follows:
    
    python instance-launch.py --instance GPU --instance Linux

The order of the flags is important, so make sure to follow it. Next up, define a keypair to use to authenticate yourself with the instance. If you haven't already created a keypair, refer to the main README for instructions. 

    python instance-launch.py --keypair [keypair-name]

The script should run and prompt for a number of inputs, including the instance type, storage amount, AMI image ID, number of instances to create and a compulsory tag to be associated with the instance. Leave blank for defaults.

The full command is

    python instance-launch.py --instance [GPU/CPU] --instance[Windows/Linux] --keypair [keypair-name]

## Connecting to instance

Now that you've launched an instance, it's time to connect to the instance. Refer [here](https://github.com/droneslab/enhance-aws/blob/master/docs/vnc-connect.md) for instructions