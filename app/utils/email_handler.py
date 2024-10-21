import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

def send_email(subject: str, recipient: str, body: str):
    msg = MIMEMultipart()
    msg["From"] = settings.EMAILS_FROM_EMAIL
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_TLS:
                server.starttls()
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAILS_FROM_EMAIL, recipient, msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")