with open('deep_learning.jpg', 'rb') as f:
                    img_data = f.read()
                    image = MIMEImage(img_data, name='deep_learning')
                    msg.attach(image)
                smtp_session = smtplib.SMTP(smtp_server, smtp_port)
                smtp_session.starttls()
                smtp_session.login(smtp_username, smtp_password)
                smtp_session.sendmail(smtp_username, receiving_email, msg.as_string())
                smtp_session.quit()
