import os
from keras.models import load_model
from pygame import mixer
from twilio.rest import Client
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import pyautogui
import cv2
import numpy as np
import boto3
resolution = (1920, 1080)
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'shanmuga@gmail.com'
smtp_password = 'cczwvznpdnidomrz'
receiving_email = 'abc@gmail.com'
subject = 'Driver who is sleeping'
msg = MIMEMultipart()
msg['From'] = smtp_username
msg['To'] = receiving_email
msg['Subject'] = subject
account_sid = 'AC47523ec6395a7d25077576b7af13e804'
auth_token = '717653b0e76dd57c0445491f9eb88c78'
client = Client(account_sid, auth_token)
to_number = '+911234567890'
from_number = '+12762959853'
twiml_url = 'http://demo.twilio.com/docs/voice.xml'
mixer.init()
sound = mixer.Sound('alarm.wav')
face = cv2.CascadeClassifier('haar cascade files\haarcascade_frontalface_alt.xml')
leye = cv2.CascadeClassifier('haar cascade files\haarcascade_lefteye_2splits.xml')
reye = cv2.CascadeClassifier('haar cascade files\haarcascade_righteye_2splits.xml')
model = load_model('models/model2.h5')
path = os.getcwd()
cap = cv2.VideoCapture(1)
font = cv2.FONT_HERSHEY_COMPLEX
count = 0
score = 0

rpred = [99]
lpred = [99]
notification=0
codec = cv2.VideoWriter_fourcc(*"XVID")
filename = "drowsiness.avi"
fps = 60.0
out = cv2.VideoWriter(filename, codec, fps, resolution)
while True:
    ret, frame = cap.read()
    height, width = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = pyautogui.screenshot()
    frame1 = np.array(img)
    out.write(frame1)
    faces = face.detectMultiScale(gray, minNeighbors=5, scaleFactor=1.1, minSize=(25, 25))
    left_eye = leye.detectMultiScale(gray)
    right_eye = reye.detectMultiScale(gray)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 1)
    for (x, y, w, h) in right_eye:
        r_eye = frame[y:y + h, x:x + w]
        count = count + 1
        r_eye = cv2.cvtColor(r_eye, cv2.COLOR_BGR2GRAY)
        r_eye = cv2.resize(r_eye, (24, 24))
        r_eye = r_eye / 255
        r_eye = r_eye.reshape(24, 24, -1)
        r_eye = np.expand_dims(r_eye, axis=0)
        rpred = np.argmax(model.predict(r_eye), axis=-1)
        break
    for (x, y, w, h) in left_eye:
        l_eye = frame[y:y + h, x:x + w]
        count = count + 1
        l_eye = cv2.cvtColor(l_eye, cv2.COLOR_BGR2GRAY)
        l_eye = cv2.resize(l_eye, (24, 24))
        l_eye = l_eye / 255
        l_eye = l_eye.reshape(24, 24, -1)
        l_eye = np.expand_dims(l_eye, axis=0)
        lpred = np.argmax(model.predict(l_eye), axis=-1)
        break
    if (rpred[0] == 0 and lpred[0] == 0):
        print(score)
        score = score + 1
        cv2.putText(frame, "Drowsy", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
    else:
        print(score)
        score = 0
        cv2.putText(frame, "", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
    if (score > 20):
        try:
            sound.play()
        except:
            pass
        cv2.imwrite(os.path.join(path, 'deep_learning.jpg'), frame)
        if (score > 30):
            notification+=1
            if (notification % 40) == 0:
                out.release()
                client_s3 = boto3.client('s3', aws_access_key_id='AKIAZLPUARLDTKFL5NBP',
                                      aws_secret_access_key='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')
                bucket = 'gabeguna579'
                file = 'drowsiness.avi'
                filename = os.path.join(path, file)
                client_s3.upload_file(filename, bucket, file,ExtraArgs={'ContentType':'video/x-msvideo','ContentDisposition':'inline'})
                url = 'https://d7wxug00sdmmf.cloudfront.net/' + file
                print(f"Use this url to see the video {url}")
                call = client.calls.create(
                to=to_number,
                from_=from_number,
                url=twiml_url)
                mes="Driver is Sleeping continuously,Please refer this video"+url
                message = client.messages.create(
                body=mes,
                from_=from_number,
                to=to_number
                )
                with open('deep_learning.jpg', 'rb') as f:
                    img_data = f.read()
                    image = MIMEImage(img_data, name='deep_learning')
                    msg.attach(image)
                smtp_session = smtplib.SMTP(smtp_server, smtp_port)
                smtp_session.starttls()
                smtp_session.login(smtp_username, smtp_password)
                smtp_session.sendmail(smtp_username, receiving_email, msg.as_string())
                smtp_session.quit()
                print('Captured image was successfully sent to the mail ID', receiving_email)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('r'):
        break

cap.release()

cv2.destroyAllWindows()
