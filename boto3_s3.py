#Loading Boto3 library
import boto3
from botocore.exceptions import ClientError

#creating client object for S3 service
#put ACCESS_KEY and SECRET_KEY of some AWS IAM user that has required permissions to access and list S3 Buckets
s3_client = boto3.client('s3', 
                      aws_access_key_id=ACCESS_KEY, 
                      aws_secret_access_key=SECRET_KEY, 
                      region_name=REGION
                      )

#fetching all the buckets in S3 and storing the output in response variable
response = s3_client.list_buckets()

#taking each bucket and checking whether it is encrypted or not
for bucket in response['Buckets']:
  
  #this try block will run only for the buckets which are encrypted otherwise the code will fail for non-encrypted buckets and then the except block will run
    try:
        
    #getting the bucket encryption type and by this we can check whether the bucket is encrypted or not using get_bucket_encryption() function and passing the bucket name to it
        enc = s3.get_bucket_encryption(Bucket=bucket['Name'])
    
    #if the above function runs successfully then fetching the bucket encryption type and algorithm
        rules = enc['ServerSideEncryptionConfiguration']['Rules']
        
    #finally printing the bucket name and its encryption type
        print('Bucket: %s, Encryption: %s' % (bucket['Name'], rules))
        
  #this except block will run when the try blcok fails and since try block has failed, so it means the bucket is not encrypted
    except ClientError as e:
        
        #with ClientError reading the type of error the code gives when it is failed and storing in e variable
        #here checking if the code fails with 'ServerSideEncryptionConfigurationNotFoundError' , it means the bucket is not encrypted
        if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
            
            #printing the bucket name with message that is it not encrypted
            print('Bucket: %s, no server-side encryption' % (bucket['Name']))
            
        else:
        #printing the bucket name if the code fails with some unknown error i.e., other than 'ServerSideEncryptionConfigurationNotFoundError' 
            print("Bucket: %s, unexpected error: %s" % (bucket['Name'], e))
