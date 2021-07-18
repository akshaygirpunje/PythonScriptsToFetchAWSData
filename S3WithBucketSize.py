#!/usr/bin/python
import boto3
client = boto3.client('s3')
resource = boto3.resource('s3')
response = client.list_buckets()
#loc_response = client.get_bucket_location(Bucket=str(response['Buckets'][i]['Name']))
#print(loc_response)
cnt = (len(response['Buckets']))
print('Name,Date_Created,BucketSize,Location')
for i in range(0,cnt):
 
    bucket = resource.Bucket(str(response['Buckets'][i]['Name']))
    total_size = 0
    for object in bucket.objects.all():
        total_size += object.size

       # print(object.size)
    #print(str(response['Buckets'][i]['Name'])+','+str(total_size))
    loc = ''
    #print(str(response['Buckets'][i]['Name'])+','+str(response['Buckets'][i]['CreationDate'])[:11])
    loc_response = client.get_bucket_location(Bucket=str(response['Buckets'][i]['Name']))
    if str(loc_response['LocationConstraint']) == 'None':
        loc = 'us-east-1'
    else:
        loc = str(loc_response['LocationConstraint'])
    name = str(response['Buckets'][i]['Name'])
    date_created = str(response['Buckets'][i]['CreationDate'])[:11]
    Bucket_Size = str(total_size)
    print(name+','+date_created+','+Bucket_Size+','+loc)
