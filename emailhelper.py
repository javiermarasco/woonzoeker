import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl


def CreateBodyHeader(body):
    bodyinner = ''
    bodyinner += '<table>'
    bodyinner += '<tr><th>Provider</th><th>Name</th><th>Location</th><th>Price</th><th>Link</th></tr>'
    return bodyinner

def CreateBodyFooter(body):
    return '</table>'

def CreateBodyLine(body,provider,entryName,entryLocation,entryPrice,entryLink):
    return '<tr><td>' + provider + '</td><td>' + entryName + '</td><td>' + entryLocation + '</td><td>' + entryPrice + '</td><td>' + entryLink + '</td></tr>'

def SendEmail(mailUser,mailPassword,mailReceiver,mailSubject,mailBody):
    sender_email = mailUser
    receiver_email = mailReceiver
    password = mailPassword
    message = MIMEMultipart("alternative")
    message["Subject"] = mailSubject
    message["From"] = sender_email
    message["To"] = receiver_email
    # Create the plain-text and HTML version of your message
    html = """\
    <html>
    <body>
        %s
    </body>
    </html>
    """ % (mailBody)
    # Turn these into plain/html MIMEText objects
    part2 = MIMEText(html, "html")
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, message["To"].split(","), message.as_string()
        )    
