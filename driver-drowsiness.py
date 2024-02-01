import cv2
import os
from keras.models import load_model
import numpy as np
from pygame import mixer

from twilio.rest import Client

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

import zmq
import base64


smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'shanmuga@gmail.com'
smtp_password = 'cczwvznpdnidomrz'
receiving_email = 'shanmuga579@gmail.com'
subject = 'Driver who is sleeping'



# create message object instance
msg = MIMEMultipart()

# setup message parameters
msg['From'] = smtp_username
msg['To'] = receiving_email
msg['Subject'] = subject

# Your Twilio account SID and auth token
account_sid = 'AC47523ec6395a7d25077576b7af13e804'
auth_token = '717653b0e76dd57c0445491f9eb88c78'
# Create a Twilio client object
client = Client(account_sid, auth_token)
# The phone number you want to call (in E.164 format)
to_number = '+919150346391'
# The Twilio phone number to use as the caller ID (in E.164 format)
from_number = '+12762959853'
# The URL of the TwiML file that will handle the call
twiml_url = 'http://demo.twilio.com/docs/voice.xml'

message = 'Sleeping for about 60 sec'

mixer.init()
sound = mixer.Sound('alarm.wav')

face = cv2.CascadeClassifier('haar cascade files\haarcascade_frontalface_alt.xml')
leye = cv2.CascadeClassifier('haar cascade files\haarcascade_lefteye_2splits.xml')
reye = cv2.CascadeClassifier('haar cascade files\haarcascade_righteye_2splits.xml')

lbl = ['Close', 'Open']

model = load_model('models/model.h5')
path = os.getcwd()
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX
count = 0
score = 0
thicc = 2
rpred = [99]
lpred = [99]
notification = 0

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://localhost:5555')

while True:
    ret, frame = cap.read()
    height, width = frame.shape[:2]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face.detectMultiScale(gray, minNeighbors=5, scaleFactor=1.1, minSize=(25, 25))
    left_eye = leye.detectMultiScale(gray)
    right_eye = reye.detectMultiScale(gray)

    # cv2.rectangle(frame, (0, height - 50), (200, height), (0, 0, 0), thickness=cv2.FILLED)

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
        if (rpred[0] == 1):
            lbl = 'Open'
        if (rpred[0] == 0):
            lbl = 'Closed'
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
        if (lpred[0] == 1):
            lbl = 'Open'
        if (lpred[0] == 0):
            lbl = 'Closed'
        break

    if (rpred[0] == 0 and lpred[0] == 0):
        print(score)
        score = score + 1
        cv2.putText(frame, "Drowsy", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imwrite(os.path.join(path, 'deep_learning.jpg'), frame)
    else:
        print(score)
        score = 0
        cv2.putText(frame, "", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

    if (score < 0):
        score = 0
    # cv2.putText(frame, 'Score:' + str(score), (100, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
    if (score > 20):
        # person is feeling sleepy so we beep the alarm
        try:
            sound.play()

        except:  # isplaying = False
            pass

        if (score > 30):
            notification += 1
            if (notification % 40) == 0:
                call = client.calls.create(
                    to=to_number,
                    from_=from_number,
                    url=twiml_url)

                message = client.messages.create(
                    body=message,
                    from_=from_number,
                    to=to_number
                )

                # Print the message SID (a unique identifier for the message)
                print(message.sid)

                # Print the call SID
                print(call.sid)
                with open('machine_learning.jpg', 'rb') as f:
                    img_data = f.read()
                    image = MIMEImage(img_data, name='deep_learning')
                    msg.attach(image)

                # create SMTP session
                smtp_session = smtplib.SMTP(smtp_server, smtp_port)

                # start TLS for security
                smtp_session.starttls()

                # login to SMTP server
                smtp_session.login(smtp_username, smtp_password)

                # send message
                smtp_session.sendmail(smtp_username, receiving_email, msg.as_string())

                # terminate SMTP session
                smtp_session.quit()

                print('Captured image was successfully sent to the mail ID', receiving_email)

            # if (thicc < 16):
            thicc = thicc + 2
        # else:
        # thicc = thicc - 2
        # if (thicc < 2):
        # thicc = 2
        # cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 0), thicc)
    encoded, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer)
    footage_socket.send(jpg_as_text)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
