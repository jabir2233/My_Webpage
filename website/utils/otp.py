import secrets

def generate_otp():
   return str(secrets.randbelow(1000000)).zfill(6)
