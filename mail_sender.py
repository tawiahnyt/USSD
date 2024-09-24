import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

PASSWORD = 'jpflqyglybrnbsjh'
EMAIL = 'mail_sendme@yahoo.com'

def registration_mail(email, name):
    sender_email = EMAIL
    receiver_email = email
    subject = "Course Registration"
    body = f"Hello {name},\nYour courses have been registered successfully.\nFind attached to this mail a copy of your registration slip."
    password = PASSWORD  # Ensure you handle passwords securely

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    filename = "pdf/SIP COURSE REGISTRATION.pdf"

    if os.path.isfile(filename):
        with open(filename, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filename)}')
            msg.attach(part)
    else:
        print(f"File {filename} does not exist.")

    try:
        with smtplib.SMTP('smtp.mail.yahoo.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def academic_calendar_mail(email, name):
    sender_email = EMAIL
    receiver_email = email
    subject = "Academic calendar"
    body = f"Hello {name},\nFind attached to this mail a copy of your Academic calendar."
    password = PASSWORD  # Ensure you handle passwords securely

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    filename = "pdf/ACADEMIC CALENDAR.pdf"

    if os.path.isfile(filename):
        with open(filename, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filename)}')
            msg.attach(part)
    else:
        print(f"File {filename} does not exist.")

    try:
        with smtplib.SMTP('smtp.mail.yahoo.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def timetable_mail(email, name):
    sender_email = EMAIL
    receiver_email = email
    subject = "Timetable"
    body = f"Hello {name},\nFind attached to this mail a copy of your lecture timetable."
    password = PASSWORD  # Ensure you handle passwords securely

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    filename = "pdf/timetable.pdf"

    if os.path.isfile(filename):
        with open(filename, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filename)}')
            msg.attach(part)
    else:
        print(f"File {filename} does not exist.")

    try:
        with smtplib.SMTP('smtp.mail.yahoo.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")


