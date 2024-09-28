import random
import re
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os, sys
from dotenv import load_dotenv


from .templateUtil import get_email_template, get_rating_email_template
load_dotenv()

smtp_host = os.getenv("SMTP_HOST", "")
smtp_port = int(os.getenv("SMTP_PORT", "587"))
smtp_user = os.getenv("SMTP_USER", "")
smtp_password = os.getenv("SMTP_PASSWORD", "")



def send_email(to_email: str, subject: str, detail: str, recommendation: str, prompt: str, isAdminister: bool,
               isDemo: bool, email_destination):
    msg = MIMEMultipart("alternative")
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject
    print(f"SMTP User: {smtp_user} , email_destination: {email_destination}")
    html_content = get_email_template(detail, recommendation, prompt, email_destination, isAdminister, isDemo)

    part2 = MIMEText(html_content, "html")

    msg.attach(part2)

    try:
        server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        server.ehlo()
        if smtp_port == 587:
            server.starttls()
            server.ehlo()

        server.login(smtp_user, smtp_password)

        response = server.sendmail(smtp_user, to_email, msg.as_string())
        print("Email sent successfully", response)
        server.close()
        time.sleep(random.uniform(1, 20))
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_rating_email(to_email: str, subject: str, rating: int, userPrompt: str, summary: str):
    msg = MIMEMultipart("alternative")
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject
    html_content = get_rating_email_template(rating, userPrompt,
                                             summary);
    part2 = MIMEText(html_content, "html")

    msg.attach(part2)
    try:
        server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        server.ehlo()
        if smtp_port == 587:
            server.starttls()
            server.ehlo()

        server.login(smtp_user, smtp_password)

        response = server.sendmail(smtp_user, to_email, msg.as_string())
        server.close()
        time.sleep(random.uniform(1, 20))
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

