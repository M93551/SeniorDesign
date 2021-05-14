import boto3

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
elbv2client = boto3.client('elbv2')

'''this is always needed for a python lambda function'''
def lambda_handler(event, context):
    
    '''filters the instances that the tag Purpose lambda'''
    filters = [{
            'Name': 'tag:Purpose',
            'Values': ['lambda']
        }
    ]
    
    ''''instances variable holds the filtered results'''
    instances = ec2.instances.filter(Filters=filters)
    
    '''response variable holds the results of the describe instances call'''
    response = client.describe_instances(Filters=filters)
    print(response)
    
    '''variable to hold the instance id of every runnning instance with the Purpose lambda tag'''
    RunningInstances = [instance.id for instance in instances]
    print(RunningInstances)
    
    '''variable to hold the call to stop the instances then the variable is printed to run the calls
    shutDown = ec2.instances.filter(InstanceIds=RunningInstances).stop()
    print (shutDown)'''
    
    '''this block puts the value of RunningInstances into a new variable that will the hold the instance id and then remove the [ ] ' characters'''
    instanceID = str(RunningInstances)
    instanceID = instanceID.replace('[', '')
    instanceID = instanceID.replace(']', '')
    instanceID = instanceID.replace("'", '')
    print(instanceID)  
    
    '''deregisters an instance from an application load balancer, instanceID is holding a string value of the instance id,
    this function can also register an instance by changing deregister_targets to register_targets, deregistering can take up to 5 minutes'''
    response = elbv2client.deregister_targets(
        TargetGroupArn='arn:aws:elasticloadbalancing:us-west-2:290943450292:targetgroup/project2/f44c702a0068c942',
        Targets=[
            {
                'Id': instanceID,
            },
        ],
    )
    