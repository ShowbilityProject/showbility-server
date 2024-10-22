import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.config import settings
import random

def send_mail_with_code(recip_list):
    subject = '쇼빌리티 인증 메일입니다.'
    code = random.randint(100000, 999999)  # 6자리 인증 코드 생성
    message = f'인증번호는 {code} 입니다.'

    msg = MIMEMultipart()
    msg['From'] = settings.EMAILS_FROM_EMAIL
    msg['To'] = ", ".join(recip_list)
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.EMAILS_FROM_EMAIL, recip_list, msg.as_string())
        server.quit()
        return code
    except Exception as e:
        print(f"Error sending email: {e}")
        return None