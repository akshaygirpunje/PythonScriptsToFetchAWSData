#!/bin/bash

#Loading the profile for PL account and get the info of Available state volumes
export AWS_PROFILE=prelogin
now=$(date +"%m_%d_%Y")
python AvailableVolumeDetails.py > /root/AvailableVolumeDetails_Prelogin_$now.csv


#Calculate total no of volumes
count1=`cat AvailableVolumeDetails_Prelogin_$now.csv | wc -l`
preloginVolumeCount=`expr $count1 - 1`


#Loading the profile for Instructure account and get the info of Available state volumes
export AWS_PROFILE=instructure
now=$(date +"%m_%d_%Y")
python AvailableVolumeDetails.py > /root/AvailableVolumeDetails_Instructure_$now.csv


#Calculate total no of volumes
count2=`cat /root/AvailableVolumeDetails_Instructure_$now.csv | wc -l`
instructureVolumeCount=`expr $count2 - 1`


#Loading the profile for china account and get the info of Available state volumes
export AWS_PROFILE=china
now=$(date +"%m_%d_%Y")
python AvailableVolumeDetails.py > /root/AvailableVolumeDetails_China_$now.csv


#Calculate total no of volumes
count3=`cat /root/AvailableVolumeDetails_China_$now.csv | wc -l`
chinaVolumeCount=`expr $count3 - 1`


#Loading the profile for outscale account and get the info of Available state volumes
export AWS_PROFILE=osprod
now=$(date +"%m_%d_%Y")
python AvailableVolumeDetails_Outscale.py > /root/AvailableVolumeDetails_ProdOutscale_$now.csv


#Calculate total no of volumes
count4=`cat /root/AvailableVolumeDetails_ProdOutscale_$now.csv | wc -l`
outscaleProdVolumeCount=`expr $count4 - 1`

#Loading the profile for outscale account and get the info of Available state volumes
export AWS_PROFILE=cdastg
now=$(date +"%m_%d_%Y")
python AvailableVolumeDetails_Outscale.py > /root/AvailableVolumeDetails_NonProdOutscale_$now.csv


#Calculate total no of volumes
count5=`cat /root/AvailableVolumeDetails_NonProdOutscale_$now.csv | wc -l`
outscaleNonProdVolumeCount=`expr $count5 - 1`


sleep 20

#Mail Trigger
echo -e "Hello Team, \n\nPFA weekly report of all unattached volumes which are in an available state from Instructure , Prelogin , China AWS accounts and outscale's prod and nonprod accounts.  \n\n#Generated on :: $now \n\n#Generated from server :: `hostname` `hostname -I` \n\n#Total number of available state volumes in a Prelogin account: $preloginVolumeCount \n\n#Total number of available state volumes in an Instructure account: $instructureVolumeCount \n\n#Total number of available state volumes in a China account: $chinaVolumeCount \n\n#Total number of available state volumes in a Production Outscale  account: $outscaleProdVolumeCount \n\n#Total number of available state volumes in a Non-Production Outscale  account: $outscaleNonProdVolumeCount  " | mail -s "Weekly report of all unattached volumes and which are in an available state" -a /root/AvailableVolumeDetails_Instructure_$now.csv -a /root/AvailableVolumeDetails_Prelogin_$now.csv -a /root/AvailableVolumeDetails_China_$now.csv  -a /root/AvailableVolumeDetails_ProdOutscale_$now.csv -a  /root/AvailableVolumeDetails_NonProdOutscale_$now.csv  emailalias@cisco.com
