#Displays the list of region,SnapshotID,OwnerId,str(VolumeSize),str(StartTime),Description

#!/usr/bin/python
import boto3

client = boto3.client('ec2')

# Get list of regions
ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
print("Region ,SnapshotID,Owner Id, VolumeSize in GiB,Created On, Description ")


# Iterate over regions
for region in ec2_regions:

    # Connect to region
    client = boto3.client('ec2', region_name=region)
    
    #Get details of snapshots in particular region.
    response = client.describe_snapshots(OwnerIds=['self'])
    no_of_snapshots = (len(response['Snapshots']))    

    #Displays the list of region,SnapshotID,OwnerId,str(VolumeSize),str(StartTime),Description
    for i in range(0, no_of_snapshots):
        SnapshotID = response['Snapshots'][i]['SnapshotId']
        VolumeSize = response['Snapshots'][i]['VolumeSize']
        OwnerId = response['Snapshots'][i]['OwnerId']
        StartTime = response['Snapshots'][i]['StartTime']        
        Description = str(response['Snapshots'][i]['Description']).replace(',','').replace(",","")
        print(region+','+SnapshotID+','+OwnerId+','+ str(VolumeSize)+','+str(StartTime)+','+Description)

