import smtplib
import ssl
from dotenv import load_dotenv
import os

load_dotenv()
MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
MAIL_SERVER = os.environ["MAIL_SERVER"]

# Email information
FROM = "alifeee.web@outlook.com"

# recipients
TO = ["alifeeerenn@hotmail.com"]  # must be a list

# Email content
SUBJECT = "Website changed"
TEXT = "A website you were tracking has changed"
message = f"""From: {FROM}
To: {", ".join(TO)}
Subject: {SUBJECT}

{TEXT}
"""

# Send the mail
server = smtplib.SMTP(MAIL_SERVER)
server.sendmail(FROM, TO, message)
server.quit()
