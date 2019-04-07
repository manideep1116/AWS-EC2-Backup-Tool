
The objective of this project is to create a tool able to perform a backup of a given directory to a data storage device in the cloud. In the process, I have learned few things about writing modular system tools, about command pipelining, the use of some common commands, and some insights into a cloud-based storage model. 
 
                                                  Man Page description:


NAME
       ec2-backup -- backup a directory into Elastic Block Storage (EBS)

SYNOPSIS
        ec2-backup [-h] [-v volume-id] dir

DESCRIPTION
        The ec2-backup tool performs a backup of the given directory into Amazon
        Elastic Block Storage (EBS).  This is achieved by creating a volume of
        the appropriate size, attaching it to an EC2 instance and finally copying
        the files from the given directory onto this volume.

OPTIONS
        ec2-backup accepts the following command-line flags:

        -h         Print a usage statement and exit.

        -v volume-id  Use the given volume instead of creating a new one.

DETAILS
        ec2-backup will perform a backup of the given directory to an EBS volume.

        ec2-backup will create an instance suitable to perform the backup, attach
        the volume in question and then back up the data from the given direc-
        tory.  Afterwards, ec2-backup will terminate the instance it created.

OUTPUT
        If successful, ec2-backup will print the volume-id of the volume to which
        it backed up the data as the only output.

        Unless the EC2_BACKUP_VERBOSE environment variable is set, ec2-backup
        will not generate any other output unless any errors are encountered.  If
        that variable is set, it may print out some useful information about what
        steps it is currently performing.

        Any errors encountered cause a meaningful error message to be printed to
        STDERR.

ENVIRONMENT
        ec2-backup assumes that the user has set up their environment for general
        use with the EC2 tools and ssh(1) without any special flags on the com-
        mand-line.     That is, the user has a suitable section in their ~/.ssh/con-
        fig file to ensure that running 'ssh ec2-instance.amazonaws.com' suc-
        ceeds.

        To accomplish this, the user has created an SSH key pair named
        'ec2-backup' and configured their SSH setup to use that key to connect to
        EC2 instances.

        ec2-backup also assumes that the user has set up their ~/.ssh/config file
        to access instances in EC2 via ssh(1) without any additional settings.
        It does allow the user to add custom flags to the ssh(1) commands it
        invokes via the EC2_BACKUP_FLAGS_SSH environment variable.


EXAMPLES
        The following examples illustrate common usage of this tool.

        To back up the entire filesystem:

        $ ec2-backup /
        vol-1a2b3c4d

        To create a complete backup of the current working directory using
        defaults to the volume with the ID vol-1a2b3c4d, possibly overwriting any
        data previously stored there:

        $ ec2-backup -v vol-1a2b3c4d .
        vol-1a2b3c4d



