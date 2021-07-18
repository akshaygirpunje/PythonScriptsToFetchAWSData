#!/usr/bin/python
import boto3

client1 = boto3.client('ec2')
elb_regions = [region['RegionName'] for region in client1.describe_regions()['Regions']]
print("Load Balancer Name,Health_Status,Count of Attached Instances,DNS Name,Created Time,Region,"+tag_details)
  
for region in elb_regions:
    conn = boto3.client('elb',region_name=region)
    elbresponse = conn.describe_load_balancers()
    elbs = elbresponse["LoadBalancerDescriptions"]    
    for elb in elbs:
        if len(elb) > 0:
            LBName=elb["LoadBalancerName"]
            healthresponse = conn.describe_instance_health(LoadBalancerName=LBName)
            healths = healthresponse["InstanceStates"]
            attchedInstances=len(healths)
            count = 0
            instancesList = []
            healthList = []
            if (attchedInstances==0):
                health= 'OutOfService'
            else:
                while count < attchedInstances:
                    health=healths[count]['State']
                    instances=healths[count]['InstanceId']
                    healthList.append(health)
                    instancesList.append(instances)
                    if 'InService' in healthList:
                        health_status= 'InService'
                    else:
                        health_status='OutOfService'
                    count += 1			


            print(elb["LoadBalancerName"]+','+health+','+str(attchedInstances)+','+str(elb["DNSName"])+','+str(elb["CreatedTime"])+','+region+','+tag_output)

