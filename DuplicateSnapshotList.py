#Displays the list of volumes and its all snapshots with creation date (In all region)
#Displays the No of Snapshots for the particular volume

#!/usr/bin/python
import boto3
client = boto3.client('ec2')

# Get list of regions
ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
print("Region ,VolumeID,Snapshot Id and Creation Time,No of Snapshots")

# Iterate over regions
for region in ec2_regions:    
        
    # Connect to region
    client = boto3.client('ec2', region_name=region)
	
    #Displays the list of volumes and its all snapshots with creation date (In particular region)
    def find_snapshots():
        
        #Get details of snapshots in particular region.
        response = client.describe_snapshots(OwnerIds=['self'])
        snapVolume={}
        
        #Iterate over each snapshot
        for snapshot in response['Snapshots']:
            
            #Get the details of snapshots
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
        #Displays the list of volumes and its all snapshots with creation date and No fo snapshots of each volume
        for volume in snapVolume:
            tempDict={}
            SnapshotsDateList=snapVolume[volume]
            #print(SnapshotsDateList)
            
            #Sort list using  "creation time" as a key             
            SnapshotsDateList.sort(key=lambda item:item['snap_date'], reverse=True)
            
            snapshotsDateListLength = len(SnapshotsDateList)
            tempList1=[]
            
            for i in range(snapshotsDateListLength):
                snapDateToString=str(SnapshotsDateList[i]['snap_date'])
                snapID=str(SnapshotsDateList[i]['snap'])
                tempDict[snapID]=snapDateToString
            tempList1.append(tempDict)
            
                     
            snapshotLength=len(snapVolume[volume])
            Snapshots=str(tempList1).replace('[','').replace(']','').replace("'"," ").replace(',',' ')          
            print(region +','+volume+','+Snapshots+','+str(snapshotLength))        
            

    find_snapshots()
