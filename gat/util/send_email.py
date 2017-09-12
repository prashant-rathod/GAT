import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from gat.util import config


# AWS Config
# iam smtp username ses-smtp-user.20170905-202640

def send_confirmation(address, path):
    info = readInfo("smtp")

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Confirm Your GAT Email"
    msg['From'] = "kuzema7@gmail.com"
    msg['To'] = "nikita.zemlevskiy@duke.edu"
    # msg['From'] = "noreply@gat.org"
    # msg['To'] = address
    url = readInfo("site")['url']
    mime_text = MIMEText(
        'You have just created your account for GAT! Please confirm your email by clicking on the following link or pasting it into your browser: ' + url + path)
    msg.attach(mime_text)

    s = smtplib.SMTP(info['email_host'], info['email_port'])
    s.starttls()
    s.login(info['email_host_user'], info['email_host_password'])
    s.sendmail("kuzema7@gmail.com", "nikita.zemlevskiy@duke.edu", msg.as_string())
    # s.sendmail("noreply@gat.org", address, msg.as_string())
    s.quit()


def readInfo(section):
    return config.config("/home/nikita/Projects/GAT/static/resources/security/database_config.ini", section)
