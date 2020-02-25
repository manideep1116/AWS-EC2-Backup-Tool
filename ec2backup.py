import subprocess
import time
import json
import argparse
import boto3
import os


#To find az of volume
def findaz(volumeid):
    return subprocess.getoutput('aws ec2 describe-volumes --volume-ids '+volumeid+ '  --query "Volumes[*].[AvailabilityZone]" --output text')


#Now two functions to create instance.
# 1) ins_comm is to store the command.
def ins_comm(i):
    return 'aws ec2 run-instances --image-id ami-0565af6e282977273 --count 1 --instance-type t1.micro --key-name ec2-backup --output json --placement AvailabilityZone=' + i

# 2) this command is to execute the command through subprocess. 
def create_ins(z):
     instance = subprocess.getoutput(ins_comm(z))
     inst_Id = json.loads(instance)['Instances'][0]['InstanceId']
     print('Instance created: '+ inst_Id)
     return inst_Id

#now we will write two other functions for attaching the volume to the created instance.
# 1)To store the command.
def attach_comm(a,b):
    return 'aws ec2 attach-volume --volume-id ' +  a +' --instance-id ' + b + ' --device /dev/sdf'

# 2)To execute the command through subprocess.
def attach_vol(c,d):
    attach = subprocess.getoutput(attach_comm(c,d))
    return attach
  
#writing functions to find public dns name
def pub(a):
    return "aws ec2 describe-instances --instance-ids " +a+" --query 'Reservations[*].Instances[*].[PublicDnsName]' --output text"

#2)second function to execute the command through subprocess.
def pub_dns(dns):
    pub_d = subprocess.getoutput(pub(dns))
    return pub_d

#function to compress the directory to .tar file
def compress(direc):
    t = subprocess.getoutput('tar cvf /tmp/backup.tar '+direc)
    return t

#function for to send file from local machine to remote using scp
def scp(dns):
    s =  subprocess.getoutput('scp -o StrictHostkeyChecking=no  /tmp/backup.tar ubuntu@'+dns+':~/backup.tar')
    return s

# Now we are writting two functions to ssh into the instance.
# 1) To store the comman to ssh includind commands to be executed after ssh.
def ssh_comm(dns):
    return 'ssh -o StrictHostkeyChecking=no ubuntu@'+dns + ' "sudo mkdir ~/bac ; sudo mkfs.ext4 /dev/xvdf ; sudo mount /dev/xvdf ~/bac/ ; sudo mv ~/backup.tar ~/bac/ ; cd ~/bac/ ; sudo tar xvf backup.tar ; echo $(ls ~/bac)"'

# 2) To execute the command through subprocess.
def ssh(Dns):
    ssh_into = subprocess.getoutput(ssh_comm(Dns))
    return ssh_into

#Now we write a function to terminate instance.
def terminate(i):
    return subprocess.getoutput('aws ec2 terminate-instances --instance-ids ' + i)

#function to take volume id from users input. If it's empty , creates one.
def run(vol_id):
    if vol_id is None:
        volId, avZone = create_new_volume(size)
        return volId
    else:
        return vol_id

#function to create volume based on given volume size
def create_new_volume(s):
    if s < 1:
        x = subprocess.getoutput('aws ec2 create-volume --size '+str(2)+' --region us-east-1 --availability-zone us-east-1a --volume-type gp2' )
    else:
        x = subprocess.getoutput('aws ec2 create-volume --size '+str(2*s)+' --region us-east-1 --availability-zone us-east-1a --volume-type gp2' )
    data = json.loads(x)
    a = data['VolumeId'] 
    b = data['AvailabilityZone']
    return a,b

#Using boto3 to find the state of instance ( this can also be done using json.loads())
def get_instance_state(EC2InstanceId):
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(EC2InstanceId)
    x =  ec2instance.state['Name']    
    return x


#to find the size of given pasth in GB
def get_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
            dir_size = round(float(total_size/1024**3))
    return dir_size



#Main function to call the required functions
if __name__ == "__main__":
    parser = argparse.ArgumentParser( 
                  description = 'Backup the data from given dir to the cloud.')
    #Creating optional argument for volume ID
    parser.add_argument('-v','--volume', metavar='V',                    
                    help= 'Enter the volume ID', default=None,
                    type=str)
    #creating positional argument for directory
    parser.add_argument('dir', help = 'Locate the directory (mandatory)')
    
    # we have executed .parse_args() to parse the input arguments and get a Namespace object that contains the user input.
    args = parser.parse_args()
   
    d = args.dir   #d is given directory
    if d:
        print(args.dir) #printing direc name
    vol_Id = args.volume  #volID is the volume id provided by user or None by default.
    size = get_size(d)
    v = run(vol_Id)      # calling functions fot volumeId, az, instance id
    print('Volume ID : '+v)
    z = findaz(v)
    i = create_ins(z)

    while (True):
        time.sleep(5)
        state = get_instance_state(i)
        if state == 'running':
             print("attaching volume")
             break
    
    attach_vol(v,i)              # volume gets attached after instance comes to running state and finds dns name followed by calling scp and ssh functions.
    pubDNS= pub_dns(i)
    compress(d)
    scp(pubDNS)
    print(ssh(pubDNS))
    print(' Hurrah!! Data from directory ('+d+') backed up to AWS cloud successfully!!')
    terminate(i) 
