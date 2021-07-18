#!/usr/bin/python
import boto3

client1 = boto3.client('ec2')
elb_regions = [region['RegionName'] for region in client1.describe_regions()['Regions']]


tag_list=[]
for region in elb_regions:
    conn = boto3.client('elb',region_name=region)
    elbresponse = conn.describe_load_balancers()
    elbs = elbresponse["LoadBalancerDescriptions"]    
    for elb in elbs:
        if len(elb) > 0:
            LBName=elb["LoadBalancerName"]
            response = conn.describe_tags(LoadBalancerNames=[LBName,],)
            tag= response["TagDescriptions"][0]["Tags"]
            count=len(tag)
            for i in range(0,count):
                tag_list.append(tag[i]['Key'])
    tag_details = str(sorted(list(set(tag_list)))).replace('[','').replace("]","").replace("'","")

print("Load Balancer Name,Health_Status,Count of Attached Instances,DNS Name,Created Time,Region,"+tag_details)
total_tag_list = sorted(list(set(tag_list))) #List of all the unique tags across all region for ELB arranged in alphabetically.
  

  
for region in elb_regions:
    conn = boto3.client('elb',region_name=region)
    elbresponse = conn.describe_load_balancers()
    elbs = elbresponse["LoadBalancerDescriptions"]    
    for elb in elbs:
        if len(elb) > 0:
            LBName=elb["LoadBalancerName"]
            healthresponse = conn.describe_instance_health(LoadBalancerName=LBName)
            tag= response["TagDescriptions"][0]["Tags"]
            count=len(tag)
            val_list=[]
            for tag_element in total_tag_list: #Loop through the all the element present in the total_tag_list
                value = ''			
                for i in range(0,count):
                    if tag[i]['Key']== tag_element:
                        value = tag[i]['Value']
                        break
                if value!='':
                    val_list.append(value)				
                else:
                    val_list.append('null')				
            tag_output = str(val_list).replace('[','').replace(']','').replace("'","")
			
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

