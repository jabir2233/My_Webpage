import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from website import GMAIL_USER, GMAIL_PASS

# Set up logging for Render
logging.basicConfig(level=logging.INFO)

def send_email(to_email, otp):
    logging.info("=== Starting OTP Email Send Process ===")
    logging.info(f"Recipient: {to_email}")
    logging.info(f"GMAIL_USER: {GMAIL_USER}")
    logging.info(f"GMAIL_PASS exists? {'Yes' if GMAIL_PASS else 'No'}")

    # Prepare email
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = 'OTP Verification for Your Account at Jabir2233'

    body = f"""
    Thanks for Signing Up to Jabir2233.
    Your OTP Verification Code is: {otp}

    If you did not request this, please ignore this email.
    Your account security is important to us. Never share your OTP with anyone.
    Please do not reply to this email.
    Thanks for staying with us!
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        logging.info("Connecting to Gmail SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # <-- Very important: prints SMTP conversation to logs
        server.starttls()
        logging.info("Logging in to Gmail SMTP...")
        server.login(GMAIL_USER, GMAIL_PASS)
        logging.info("Sending email...")
        server.send_message(msg)
        server.quit()
        logging.info("Email sent successfully!")

    except smtplib.SMTPAuthenticationError as auth_err:
        logging.error(f"SMTP Authentication Error: {auth_err}")
    except smtplib.SMTPConnectError as conn_err:
        logging.error(f"SMTP Connection Error: {conn_err}")
    except smtplib.SMTPRecipientsRefused as r_err:
        logging.error(f"Recipient Refused: {r_err}")
    except smtplib.SMTPException as smtp_err:
        logging.error(f"General SMTP Error: {smtp_err}")
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")

    logging.info("=== OTP Email Process Finished ===\n")
