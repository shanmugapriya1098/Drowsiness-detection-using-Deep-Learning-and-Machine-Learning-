from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
import os
from pygame import mixer

from twilio.rest import Client

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'shanmu123@gmail.com'
smtp_password = 'cczwvznpdnidomrz'
receiving_email = 'shanmu123@gmail.com'
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
to_number = '[add number]'
# The Twilio phone number to use as the caller ID (in E.164 format)
from_number = '+12762959853'
# The URL of the TwiML file that will handle the call
twiml_url = 'http://demo.twilio.com/docs/voice.xml'

message = 'Sleeping for about 60 sec'

mixer.init()
sound = mixer.Sound('alarm.wav')

path = os.getcwd()

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

notification=0
thresh = 0.25
frame_check = 20
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")  # Dat file is the crux of the code

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
cap = cv2.VideoCapture(0)
flag = 0
while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subjects = detect(gray, 0)
    for subject in subjects:
        shape = predict(gray, subject)
        shape = face_utils.shape_to_np(shape)  # converting to NumPy Array
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        if ear < thresh:
            flag += 1
            print(flag)
            if flag >= frame_check:
                cv2.putText(frame, "Drowsy", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                cv2.imwrite(os.path.join(path, 'machine_learning.jpg'), frame)
                try:
                    sound.play()

                except:  # isplaying = False
                    pass
                if flag >= 30:
                    notification += 1
                    if (notification % 60) == 0:
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
                            image = MIMEImage(img_data, name='machine_learning')
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
                        image = MIMEImage(img_data, name='machine_learning')
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

        else:
            flag = 0
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cv2.destroyAllWindows()
cap.release()

