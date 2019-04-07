-->To execute unix commands in Python we have package called "os".
--> By importing os we can use statements like "system" to execute commands.
Ex: os.system("ls -s")
--> We have package called "subprocess" which replaces "os".
Ex: subprocess.call("ls", shell=True)
  -->By using subprocess, we can communicate with shell from our python script. It basically executes the commands on shell and will get output from our python script.
  --> In the above example, it is calling "ls" commmand. "shell = True" means it is doing everything in the shell.
--> To store the output in a variable using subprocess.
Ex: output = subprocess.check_output("ls", shell=True)
  (this gives output as bytes)
--> We have subprocess.getoutput(cmd) to give output as string.
--> we have json.loads() to parse the string type to dictionary in python.
-->We can also use subprocess.check_output() but the subprocess gives the output in bytes. We need to give the output of this command as input in next subprocess command which requires input as string. So , to get the output from subprocess as string, we are using subprocess.getoutput().




-->This is for json.loads()
#Now we need the instanceId. So, the output string can be parsed(changing the data structure to store data) to JSON to extract the id easily using json.loads() function. But in python we dont have json. So, we get output in the form of dictionary. In that dictinary we may have list in the values and in that lists we may have dictionaries.So here: 
--> output of inst is string format.
>> type(inst)
<class 'str'>
--> let parsedint = json.loads(inst)
>>type(parsedinst)
<class 'dict'>
 >>parsedinst.keys()
 dict_keys(['Groups', 'Instances', 'OwnerId', 'ReservationId'])
-->now will take the key 'Instances
>>type(parsedinst['Instances'])
<class 'list'>
-->Types of all the keys:
    >> type(parsedinst['Groups'])
    <class 'list'>
    >> type(parsedinst['Instances'])
    <class 'list'>
    >> type(parsedinst['OwnerId'])
    <class 'str'>
    >> type(parsedinst['ReservationId'])
    <class 'str'>
--> Now in Instances list we have one item, which is dictionary.
>> type(parsedinst['Instances'][0])
<class 'dict'>
--> Now will retrieve our required instanceId which is the value of the key 'InstanceID'
> parsedinst['Instances'][0]['InstanceId']
'i-030f31cf7a1b76344'

# inst_Id = json.loads(inst)['Instances'][0]['InstanceId']

