#!/usr/bin/python
import boto3
import datetime

client = boto3.client('ec2')
ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

print("Region,Instance_ID,Instance_Name,Instance_Type,Instance_State")

for region in ec2_regions:
    conn = boto3.resource('ec2',region_name=region)
    instances = conn.instances.filter()    
    for instance in instances:        
        if instance.tags is not None:
            for tags in instance.tags:
                if tags["Key"] == 'Name':
                    instancename = tags["Value"]
        print(region+','+instance.id+','+instancename+','+instance.instance_type+','+str(instance.state['Name']))
        