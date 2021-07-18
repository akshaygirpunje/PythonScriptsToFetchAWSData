#Displays the list of Snapshot not Attached To any AMI

#!/usr/bin/python
import boto3
client = boto3.client('ec2')

# Get list of regions
ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

print("SnapshotsNotAttachedToAnyAMI")
SnapshotFinalList=[]
AMIAttachedSnapshotFinalList=[]

# Iterate over regions
for region in ec2_regions:

    # Connect to region
    client = boto3.client('ec2', region_name=region)
    
    #Get a details of images
    response = client.describe_images(Owners=['self']) 
    no_of_images = (len(response['Images']))
    
    responseSnapshot = client.describe_snapshots(OwnerIds=['self'])
    no_of_snapshots = (len(responseSnapshot['Snapshots']))    
    
    
    #Get the list of snapshot ID attached to AMI
    for i in range(0,no_of_images):
        ImageId = response['Images'][i]['ImageId']
        ImageName = response['Images'][i]['Name']
        ImageDescription = response['Images'][i]['Description']
        ImageCreationDate = response['Images'][i]['CreationDate']        
        no_of_BlockDeviceMappings=(len(response['Images'][i]['BlockDeviceMappings']))
        #print(str(no_of_BlockDeviceMappings))
        snapshotList=[]
        
        for j in range(0,no_of_BlockDeviceMappings):
            try:
                snapshotId = response['Images'][i]['BlockDeviceMappings'][j]['Ebs']['SnapshotId']
                AMIAttachedSnapshotFinalList.append(snapshotId)
                snapshotList.append(snapshotId)                
                Snapshots=str(snapshotList).replace('[',' ').replace(']',' ').replace("'"," ").replace(',',' ')
            except KeyError:
                continue
        
#Get the list of snapshot not attached to any AMI        
SnapshotNotAttachedToAMI=list(set(SnapshotFinalList).symmetric_difference(set(AMIAttachedSnapshotFinalList)))

#Get the count of AMIAttachedSnapshotPresent,TotalNoOfSnapshotPresent,TotalNoOfSnapshotNotAttachedToAMI
AMIAttachedSnapshotPresent=len(AMIAttachedSnapshotFinalList)
TotalNoOfSnapshotPresent=len(SnapshotFinalList)
TotalNoOfSnapshotNotAttachedToAMI=len(SnapshotNotAttachedToAMI)

# Displays the list of Snapshot Not Attached To any AMI
for snapshot in range(0,TotalNoOfSnapshotNotAttachedToAMI):
    print(str(SnapshotNotAttachedToAMI[snapshot]))

print("TotalNoOfSnapshotPresent:{}".format(str(TotalNoOfSnapshotPresent)))
print("TotalNoOfSnapshotsAttachedToAMI:{}".format(str(AMIAttachedSnapshotPresent)))
print("TotalNoOfSnapshotNotAttachedToAMI:{}".format(str(TotalNoOfSnapshotNotAttachedToAMI)))