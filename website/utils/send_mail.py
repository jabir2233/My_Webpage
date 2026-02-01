import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from website import GMAIL_USER, GMAIL_PASS

def send_email(to_email, otp):
  #Debuging Only for Render
  print("GMAIL_USER:", GMAIL_USER)
  print("GMAIL_PASS:", bool(GMAIL_PASS))

  msg = MIMEMultipart()
  msg['From'] = GMAIL_USER
  msg['To'] = to_email
  msg['Subject'] = 'OTP Verification for Your Account at Jabir2233'

  body = f'Thanks for Signing Up to Jabir2233.\nYour OTP Verification Code is: {otp}\nIf you did not request this, please ignore this email.\nYour account security is important to us. Never share your OTP with anyone.\nPlease do not reply to this email.\nThanks for staying with us!'
  msg.attach(MIMEText(body, 'plain'))

  try:
    server= smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASS)
    server.send_message(msg)
    server.quit()
    print('Email sent successfully!')
    
  except Exception as e:
    print(f'Failed to send email: {e}')

