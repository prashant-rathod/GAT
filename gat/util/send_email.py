import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# AWS Config
#iam smtp username ses-smtp-user.20170905-202640
EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_HOST_USER = 'AKIAIFHXO2MCMQTLREGA'
EMAIL_HOST_PASSWORD = 'AroMyRD79cJXfbV8jXaf8EfgRCe1vzDEnWcF37uLB0Di'
EMAIL_PORT = 587

msg = MIMEMultipart('alternative')
msg['Subject'] = "test foo"
msg['From'] = "kuzema7@gmail.com"
msg['To'] = "nikita.zemlevskiy@duke.edu"


mime_text = MIMEText('TEST TEXT')
msg.attach(mime_text)

s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
s.starttls()
s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
s.sendmail("kuzema7@gmail.com", "nikita.zemlevskiy@duke.edu", msg.as_string())
s.quit()