import os
import boto3
import webbrowser
"""import cv2
import numpy as np
import pyautogui
import time
SCREEN_SIZE=(1920,1080)
fourcc=cv2.VideoWriter_fourcc(*"XVID")
out=cv2.VideoWriter('drowsiness.avi',fourcc,20.0,(SCREEN_SIZE))
fps=120
prev=0
while True:
    time_elapsed=time.time()-prev
    img=pyautogui.screenshot()
    if time_elapsed>1.0/fps:
        prev=time.time()
        frame=np.array(img)
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    cv2.waitKey(0)
cv2.destroyAllWindows()
out.release()"""
client=boto3.client('s3',aws_access_key_id='AKIAZLPUARLDTKFL5NBP',aws_secret_access_key='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')
bucket='shanmu123'
cur_path=os.getcwd()
file='y2mate.com - How to work in Photoshop ._0djp_WKtuKQ_360p.mp4'
filename=os.path.join(cur_path,file)
data=open(filename,'rb')
client.upload_file(filename,bucket,file,ExtraArgs={'ContentType':'video/x-msvideo','ContentDisposition':'inline'})
url='http://d7wxug00sdmmf.cloudfront.net/'+file
print(f"Use this url to see the video {url}")
#webbrowser.open(url)
s3 = boto3.client('s3',

                  aws_access_key_id="AKIAZLPUARLDTKFL5NBP",

                  aws_secret_access_key="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",



                  )

key = 'drowsiness.avi'

creds = s3.generate_presigned_post(

    Bucket="shanmu123",

    Key=key,

    Fields={'ContentType':'video/x-msvideo'},

    Conditions=[{'ContentType':'video/x-msvideo'}],

    ExpiresIn=3600)
print(creds)