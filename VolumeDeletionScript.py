# Delete the snapshots pass in the "deleteSnapshotIDList"

#!/usr/bin/python
import boto3

# Connect to 'ap-southeast-1 'region
ec2 = boto3.resource('ec2',region_name='ap-southeast-1')

# Iterate over volumes
for vol in ec2.volumes.all():

    # Delete the volume if its state is available and it does not contains any tags
    if  vol.state=='available':
        if vol.tags is None:
           vid=vol.id
           v=ec2.Volume(vol.id)
           v.delete()
           print( "Successfully deleted Volume with ID:{0} ".format(vid))
           continue
           
    # Delete the volume if its state is available and it does not contains tag with Key=Name and Value=DND       
    for tag in vol.tags:
       if tag['Key'] == 'Name':
           value=tag['Value']
           if value != 'DND' and vol.state=='available':
               vid=vol.id
               v=ec2.Volume(vol.id)
               v.delete()
               print( "Successfully deleted Volume with ID :{0} ".format(vid))