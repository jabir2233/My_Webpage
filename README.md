# **Jabir2233 | Portfolio Web App**  
Personal portfolio website built with Flask (Python backend) that also includes a complete authentication system for users.
Deployed in production with Render + PostgreSQL + Brevo Email API.  
  
🔗 Live Site: __https://jabir2233.onrender.com ↗️__  
  
## ✨ Features  
• Portfolio website
• User Sign Up / Sign In
• Secure password hashing (one-way encryption)
• Google OAuth login
• Email OTP verification system
• Resend OTP with timer
• Flash messages & session handling
• PostgreSQL database (Render Cloud)
• Production deployment ready  
  
## 🛠 Tech Stack  
Backend → Flask, SQLAlchemy
Frontend → HTML, CSS, JavaScript
Auth → Flask-Login, Google OAuth
Email → Brevo (SMTP/API)
Database → PostgreSQL (Render)
Hosting → Render  
  
## 📂 Project Structure  
  
main.py  
  
instance/  
 └─ database.db (local only)  
  
website/  
 ├─ __init__.py       → App factory (create_app)  
 ├─ auth.py           → Authentication routes  
 ├─ views.py          → General routes  
 ├─ models.py         → Database models  
 ├─ static/           → CSS, JS, images  
 │   ├ *.css  
 │   └─ *.js  
 ├─ templates/  
 │   ├─ email/  
 │   │   └─ otp.html  
 │   └─ *.html  
 └─ utils/            → Utilization Programs  
       ├─ otp.py  
       └─ send_mail.py  
  
## 🔑 Environment Variables  
  
SESSION_SECRET  
DATABASE_URL  
  
GOOGLE_CLIENT_ID  
GOOGLE_CLIENT_SECRET  
  
GMAIL_USER  
GMAIL_PASS  
  
BREVO_API_KEY  
  
## 🌐 Routes  
General  
   /                     → Home (Portfolio)  
   /sign_in_up           → Login & Register  
   /verify_email         → OTP Verification  
   /google_login       → Google Login  
   /google_login/authorize  
   /logout  
  
Dev (optional)  
   /clear_database_xxx  
   /view_database_xxx  
  
## ▶ Run Locally  
Install dependencies:  
    pip install -r requirements.txt  
Run:  
    python main.py  
  or,  
    gunicorn main:app  
  
## 📧 Email System  
Provider → Brevo  
Free Tier → 300 emails/month  
Templates:  
   website/templates/email/  
Logic:  
   website/utils/send_mail.py  
  
## 💾 Backup & Versioning  
Create clean zip:  
   zip -r version/v1.0.zip main.py website requirements.txt README.md  
  
## 🗃 Git Commands  
git status  
git add .  
git commit -m "message"  
git push origin master  
  
## 👤 Author  
Jabir Hossain  
Student Developer | Flask & Python Enthusiast  
  
##### ©All The Copyrights are Reserved©
