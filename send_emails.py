'''
What: send_emails.py allows emails to be sent to and smtp email server
        given the proper parameters described in the sendEmails function.
        This function is used to send an notification email when the
        securityCamera does not recognize a face.
Who: Chris Punt and Nate Herder
When: 04/29/2020
Why: CS 300 Calvin University
'''

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def connectToEmail(sender, senderPassword, smtp, port):
    server = smtplib.SMTP(smtp, port)
    server.ehlo()
    server.starttls()

    try:
        print("logging into email")
        server.login(sender, senderPassword)
    except Exception as e:
        print("Unable to login to email")
        print(e)
        server.quit()

    return server



def sendEmail(server, sender, receiver, subject, body):

    fromaddr = sender
    toaddr = receiver
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject # "Failed Authentication Alert"

    body = body

    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)