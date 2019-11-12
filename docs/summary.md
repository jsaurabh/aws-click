## Summary 

Summary of functionality of each script

### instance-launch.py
Creates a new instance with the supplied command line arguments. Comes with a good set of defaults. 

Setting DryRun will do a dry run of the supplied arguments without executing them and return if it encounters an error.

Arguments:

    *1. --instance, --i: [GPU|CPU]
    *2. --instance, -i: [Windows|Linux]
    *3. --keypair: [keypair-name]
    4. --dry: [True]

Defaults:

    1. Type: GPU g3s.xlarge
    2. StorageL 300 GB
    3. AMI ID: Configured to use Linux GPU as default
    4. Count: Number of instances to create in one pass
    
The script will allocate an elastic IP address(static IP) and associate it with the instance. 

### instance-info.py
Writes basic set of instance info to a **config.ini** for easy lookup later on

Arguments:

    *1. --state, -s: [running|stopped|terminated]

**NOTE**: Terminated instances only show up for upto 2 hours after termination. 

### instance-manage.py
Enable/disable detailed monitoring on running instance. Useful to monitor execution of long running compute intensive jobs.

Detailed Monitoring: Collect and track usage metrics, collect and monitor log files, set alarms and setup up hooks for events in 1 minute intervals. **Paid** service

Basic Monitoring: CPU load, disk and network I/O at 5 minute intervals

Describe: 

Options:

    1. --monitor, -m: [on|off]
    2. --describe, -d: [True]

### instance-networking.py
Create, delete and describe security groups associated with the account

Options:

    1. --create, -c: [Name]
    2. --delete, -d: 
    3. --describe, --d : [Name]

### instance-state.py
Used to manage instance state. Can be used to start, stop, reboot and terminate instances

Arguments:
    
    *1. --action, -a: [on|off|reboot|terminate]
        prompts user to choose an instance ID from config.ini
    2. --dry : [True]

### keypair.py
Create and delete keypairs

Options:

    1. --create, -c: [name]
        creates keypair and stores public key locally within working directory
    2. --delete, -d: [name]



