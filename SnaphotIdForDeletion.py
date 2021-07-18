#Displays the list of snapshots other than the latest snapshots of particular volume

#!/usr/bin/python
import boto3

client = boto3.client('ec2')

# Get list of regions
ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
print("Region ,VolumeID,Snapshot Id and Creation Time")


# Iterate over regions
for region in ec2_regions:

    # Connect to region
    client = boto3.client('ec2', region_name=region)
    
    #Displays the list of snapshots other than the latest snapshots of particular volume
    def find_snapshots():
        
        #Get details of snapshots in particular region.
        response = client.describe_snapshots(OwnerIds=['self'])
        
        snapVolume={}
        
        #Iterate over each snapshot
        for snapshot in response['Snapshots']:
            snapList=[]
            snapCreationList=[]            
            SnapIDCreationTimeDict={}
            snapshot_date = snapshot['StartTime']
            snapshot_volume = snapshot['VolumeId']
            snapshot_id = snapshot['SnapshotId']            
            SnapIDCreationTimeDict['snap']=snapshot_id
            SnapIDCreationTimeDict['snap_date']=snapshot_date
            
            #Create lists of snapshots and creation time for a particular volume            #{volume1:[{snap:snapid,date:time},{snap:snapid,date:time}],volume2:[{snap:snapid,date:time},{snap:snapid,date:time}]}            
            if snapshot_volume in snapVolume:
                snapCreationList.append(SnapIDCreationTimeDict)
                list1=snapVolume[snapshot_volume]
                list1.append(SnapIDCreationTimeDict)
            else:               
                snapCreationList.append(SnapIDCreationTimeDict)                
                snapVolume[snapshot_volume]=snapCreationList
            
        #Iterate over volume
        #Displays the list of snapshots other than the latest snapshots of particular volume         
        for volume in snapVolume:
            tempDict={}
            SnapshotsDateList=snapVolume[volume]            
            
            #Sort list using  "creation time" as a key 
            SnapshotsDateList.sort(key=lambda item:item['snap_date'], reverse=True)
            
            snapshotsDateListLength = len(SnapshotsDateList)
            tempList1=[]
            tempList2=[]
            for i in range(snapshotsDateListLength):
                snapDateToString=str(SnapshotsDateList[i]['snap_date'])
                snapID=str(SnapshotsDateList[i]['snap'])
                tempDict[snapID]=snapDateToString
            tempList1.append(tempDict)
            
            snapList=[]
            snapList=list(tempDict.keys())
            
            for i in range(1,len(snapList)):
                duplicateSnapshotID=snapList[i]
                print(region +','+volume+','+duplicateSnapshotID)

    find_snapshots()
