#!/usr/bin/python
import boto3
import datetime

client = boto3.client('ec2')
ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
#print("Instance_ID,Instance_Type,Region,Instance_Name,Creator,Environment_Tag,Ordinal,Product_Code,Customer_Name,Service_ID,Hardware_Class,Autoscaling_GroupName,Cloudformation_LogicalID,Cloudformation_StackID,Cloudformation_StackName,Control,Object_Role,CPU_Usage_Daily,CPU_Usage_Weekly,CPU_Usage_Monthly")
tag_list=[]
for region in ec2_regions:
    conn = boto3.resource('ec2',region_name=region)
    instances = conn.instances.filter()    
    for instance in instances:
        if instance.tags is not None:	
            count=(len(instance.tags))
            for i in range(0,count):
                tag_list.append(instance.tags[i]['Key'])
            # for i in range(0,count):
                # tag_list.append(tag[i]['Key'])
#print(sorted(list(set(tag_list))))				
tag_details = str(sorted(list(set(tag_list)))).replace('[','').replace("]","").replace("'","")
#print(tag_details)
print("Instance_ID,Instance_Type,Region,"+tag_details)

total_tag_list = sorted(list(set(tag_list)))

for region in ec2_regions:
    conn = boto3.resource('ec2',region_name=region)
    instances = conn.instances.filter()    
    for instance in instances:        
        cw = boto3.client('cloudwatch',region_name=region)
        st = cw.get_metric_statistics(
                Period=300,
                StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=86400),
                EndTime=datetime.datetime.utcnow(),
                MetricName='CPUUtilization',
                Namespace='AWS/EC2',
                Statistics=['Average'],
                Dimensions=[{'Name':'InstanceId', 'Value':instance.id}]
                )
        st_weekly = cw.get_metric_statistics(
                Period=3600,
                StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=604800),
                EndTime=datetime.datetime.utcnow(),
                MetricName='CPUUtilization',
                Namespace='AWS/EC2',
                Statistics=['Average'],
                Dimensions=[{'Name':'InstanceId', 'Value':instance.id}]
                )
        st_monthly = cw.get_metric_statistics(
                Period=86400,
                StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=2592000),
                EndTime=datetime.datetime.utcnow(),
                MetricName='CPUUtilization',
                Namespace='AWS/EC2',
                Statistics=['Average'],
                Dimensions=[{'Name':'InstanceId', 'Value':instance.id}]
                )
        				
        
        if len(st['Datapoints']) == 0:
            cpu_usage='NA'
        else:
            cpu_usage=st['Datapoints'][0]['Average']

        if len(st_weekly['Datapoints']) == 0:
            cpu_usage_weekly='NA'
        else:
            cpu_usage_weekly=st_weekly['Datapoints'][0]['Average']

        if len(st_monthly['Datapoints']) == 0:
            cpu_usage_monthly='NA'
        else:
            cpu_usage_monthly=st_monthly['Datapoints'][0]['Average']
			
        if instance.tags is not None:
            count=(len(instance.tags))
            val_list=[]
            for tag_element in total_tag_list: #Loop through the all the element present in the total_tag_list
                value = ''		
                for i in range(0,count):
                    if instance.tags[i]['Key']==tag_element:
                        value = instance.tags[i]['Value']
                        break
                if value!='':               			
                    val_list.append(value)
                else:
                    val_list.append('null') 			
            tag_output = str(val_list).replace('[','').replace(']','').replace("'","")
            print(instance.id+','+instance.instance_type+','+region+','+tag_output)			
		
		#print(len(instance.tags))	
			
        # creator = ''
        # env_tag = ''
        # Hardware_Class = ''
        # Ordinal = ''
        # Product_Code = ''
        # Customer_Name = ''
        # Service_ID = ''
        # autoscaling_groupName = ''
        # cloudformation_logical_id = ''
        # cloudformation_stack_id = ''
        # cloudformation_stack_name = ''
        # Control = ''
        # instancename = ''
        # Object_Role = ''        
        # if instance.tags is not None:
            # for tags in instance.tags:
                # if tags["Key"] == 'Name':
                    # instancename = tags["Value"]
                # if tags["Key"] == 'Creator':
                    # creator = tags["Value"]
                # if tags["Key"] == 'Environment Type':
                    # env_tag = tags["Value"]
                # if tags["Key"] == 'Hardware Class':
                    # Hardware_Class = tags["Value"]
                # if tags["Key"] == 'Ordinal':
                    # Ordinal = tags["Value"]
                # if tags["Key"] == 'Product Code':
                    # Product_Code = tags["Value"]
                # if tags["Key"] == 'Customer Name':
                    # Customer_Name = tags["Value"]
                # if tags["Key"] == 'Service ID':
                    # Service_ID = tags["Value"]
                # if tags["Key"] == 'aws:autoscaling:groupName':
                    # autoscaling_groupName = tags["Value"]
                # if tags["Key"] == 'aws:cloudformation:logical-id':
                    # cloudformation_logical_id = tags["Value"]
                # if tags["Key"] == 'aws:cloudformation:stack-id':
                    # cloudformation_stack_id = tags["Value"]
                # if tags["Key"] == 'aws:cloudformation:stack-name':
                    # cloudformation_stack_name = tags["Value"]
                # if tags["Key"] == 'Control':
                    # Control = tags["Value"]                
                # if tags["Key"] == 'Object Role':
                    # Object_Role = tags["Value"]
        # print(instance.id+','+instance.instance_type+','+region+','+instancename+','+creator+','+env_tag+','+Ordinal+','+Product_Code+','+Customer_Name+','+Service_ID+','+Hardware_Class+','+autoscaling_groupName+','+cloudformation_logical_id+','+cloudformation_stack_id+','+cloudformation_stack_name+','+Control+','+Object_Role+','+str(cpu_usage)+','+str(cpu_usage_weekly)+','+str(cpu_usage_monthly))
 