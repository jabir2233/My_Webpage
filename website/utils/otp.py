import secrets
from werkzeug.security import generate_password_hash, check_password_hash

def generate_otp():
   return str(secrets.randbelow(1000000)).zfill(6)

def hash_otp(otp):
  return generate_password_hash(otp, method='pbkdf2:sha256')

def verify_otp(hashed_otp, user_otp):
  return check_password_hash(hashed_otp, user_otp)