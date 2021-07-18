#Displays the list of region,volume.id,volume.state,volume.size,volume.create_time

#!/usr/bin/python
import boto3
client = boto3.client('ec2')

# Get list of regions
ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
print("Region ,VolumeID,Volume State,Volume Size,Volume Creation Time")

# Iterate over regions
for region in ec2_regions:

    # Connect to region
    ec2 = boto3.resource('ec2',region_name= region)
    
    #Get a list of all volumes
    volume_iterator = ec2.volumes.all()
    
	#Get a list of available volumes
    #volume_iterator = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}])
	
	#Get a list of in-use volumes
	#volume_iterator = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['in-use']}])

    for volume in volume_iterator:
        #for attached in volume.attachments:
        print (region+','+volume.id+','+volume.state+','+str(volume.size)+','+str(volume.create_time))