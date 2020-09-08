#python 3.7 using boto3 to handle image uploads to aws S3

from secrets import access_key, secret_access_key
import boto3
import os

#client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key) #client is another approach of using aws but is low-level

s3 = boto3.resource('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)


for files in os.listdir('./images'):
    
    uplaod_file_bucket = 'smartstreetlight' #our s3 bucket 
    upload_file_key = 'images/' + str(files) #we are gonna put the file within a folder in our bucket called images

    #s3.Bucket('uplaod_file_bucket').put_object(Key='upload_file_key', Body=files, ContentType='jpg/png', ACL='public-read') #did not work
    #s3.Bucket(uplaod_file_bucket).put_object(Key=upload_file_key, Body=files, ContentType='image/png', ACL='public-read') #did not work
    #client.upload_file('images/' + files, uplaod_file_bucket, upload_file_key) #did not work
 
    s3.meta.client.upload_file(upload_file_key, uplaod_file_bucket, upload_file_key, ExtraArgs={'ContentType': "image/png", 'ACL': "public-read"} )
    #the format of upload_file is upload_file(Filename, Bucket, Key, ExtraArgs=None, Callback=None, Config=None)

    #for twilio to work you must send a acceptable content type they only accept the forms jpg, png, gif. 
    #by default aws s3 sets the content type to binary/octet-stream need to change this using the extraargs and passing custom content type
    #for jpeg/jpg use 'ContentType': "image/jpeg"

    #an example url https://smartstreetlight.s3.amazonaws.com/images/car.png 
    #smartstreetlight is our bucket name

    url = f'https://s3.amazonaws.com/{uplaod_file_bucket}/{upload_file_key}'

    print('uploaded image')
    print('\n')
    print(url)



''''

the url for the image needs to be self made use this 

media_url = f'https://smartstreetlight.s3.amazonaws.com/{upload_file_key}' 

     media_url = "https://s3.amazonaws.com/{0}" /
                            "/{1}".format(self.s3_bucket,
                                          s3_key.key)


'''