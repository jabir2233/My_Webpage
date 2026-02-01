import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from website import GMAIL_USER, GMAIL_PASS
import smtplib

# Configure logging to show info and errors
logging.basicConfig(level=logging.INFO)

def send_email(to_email, otp):
    logging.info(f"GMAIL_USER: {GMAIL_USER}")
    logging.info(f"GMAIL_PASS set? {bool(GMAIL_PASS)}")

    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = 'OTP Verification for Your Account at Jabir2233'

    body = f'Thanks for Signing Up.\nYour OTP is: {otp}'
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # <-- Shows detailed SMTP communication in logs
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()
        logging.info('Email sent successfully!')

    except Exception as e:
        logging.error(f'Failed to send email: {e}')

