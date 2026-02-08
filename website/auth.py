from flask import Blueprint, render_template, request, flash, redirect, url_for, session, render_template
from flask import current_app
from .models import User, PendingUser
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, oauth
from flask_login import login_user, login_required, logout_user, current_user
from website.utils.send_mail import send_email
from website.utils.otp import generate_otp, verify_otp, hash_otp
from datetime import datetime, timedelta
import threading
import os

auth = Blueprint('auth', __name__)

# ==============================
# Create real user
# ==============================
def create_user(username, email, password, already_hashed=False):
    if not already_hashed:
        password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = User(
        username=username,
        email=email,
        password=password
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user


# ==============================
# Create pending user
# ==============================
def create_pending_user(username, email, password, otp):
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    hashed_otp = generate_password_hash(otp, method='pbkdf2:sha256')

    new_pending_user = PendingUser(
        username=username,
        email=email,
        password=hashed_password,
        hashed_otp=hashed_otp,
        otp_expiry=datetime.now() + timedelta(minutes=5)
    )

    db.session.add(new_pending_user)
    db.session.commit()
    return new_pending_user


# ==============================
# Sign in / Sign up route
# ==============================
@auth.route('/sign_in_up', methods=['GET', 'POST'])
def sign_in_up():

    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':

        form_type = request.form.get('form_type')
        username = request.form.get('Username', '').strip()
        email = request.form.get('Email', '').strip()
        password = request.form.get('Password', '').strip()
        confirm_password = request.form.get('CPassword', '').strip()

        # ---------------- LOGIN ----------------
        if form_type == 'login':

            if not email or not password:
                flash('Email and password are required.', 'error')
                return redirect(url_for('auth.sign_in_up'))

            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))

            flash('Invalid email or password.', 'error')


        # ---------------- SIGNUP ----------------
        elif form_type == 'signup':

            if not username or not email or not password or not confirm_password:
                flash('All fields are required.', 'error')

            elif User.query.filter_by(email=email).first():
                flash('Email already exists.', 'error')

            elif len(username) < 3:
                flash('Username must be at least 3 characters.', 'error')

            elif password != confirm_password:
                flash('Passwords do not match.', 'error')

            else:
                otp = generate_otp()

                create_pending_user(username, email, password, otp)

                # store only email in session
                session['pending_users_email'] = email

                threading.Thread(
                    target=send_email,
                    args=(
                        current_app._get_current_object(),
                        email,
                        "OTP Verification for Jabir2233",
                        "email/otp.html"
                    ),
                    kwargs={
                        "username": username,
                        "otp_code": otp
                    },
                    daemon=True
                ).start()

                flash('OTP sent to your email.', 'success')
                return redirect(url_for('auth.verify_email'))

    return render_template('sign_in_up.html')


# ==============================
# Verify Email route
# ==============================
@auth.route('/verify_email', methods=['GET', 'POST'])
def verify_email():

    email = session.get('pending_users_email')
    if not email:
        return redirect(url_for('auth.sign_in_up'))

    pending = PendingUser.query.filter_by(email=email).first()
    if not pending:
        session.pop('pending_users_email', None)
        return redirect(url_for('auth.sign_in_up'))

    # ---------- OTP Expiry check ----------
    if datetime.now() > pending.otp_expiry:
        db.session.delete(pending)
        db.session.commit()
        session.pop('pending_users_email', None)
        flash("OTP expired. Please sign up again.", "error")
        return redirect(url_for('auth.sign_in_up'))

    # ---------- Verify ----------
    if request.method == 'POST':

        user_otp = request.form.get('otp', '').strip()

        if verify_otp(pending.hashed_otp, user_otp):

            new_user = create_user(
                pending.username,
                pending.email,
                pending.password,
                already_hashed=True
            )

            db.session.delete(pending)
            db.session.commit()

            session.pop('pending_users_email', None)

            login_user(new_user, remember=True)
            flash("Email verified successfully!", "success")

            return redirect(url_for('views.home'))

        flash("Incorrect OTP.", "error")

    return render_template('verify.html', email=pending.email)

@auth.route('/google_login')
def google_login():
    redirect_uri = url_for('auth.google_authorize', _external=True, _scheme='https')
    return oauth.google.authorize_redirect(redirect_uri)

@auth.route('/google_login/authorize')
def google_authorize():
    try:
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo')
        if not user_info:
            raise ValueError("User info not found")

        email = user_info.get('email')
        username = user_info.get('name')

        if not email or not username:
            flash('Failed to get info from Google.', category='error')
            return redirect(url_for('auth.sign_in_up'))

        user = User.query.filter_by(email=email).first()
        if user:
            login_user(user, remember=True)
        else:
            # Generate random password for new Google user
            new_user = create_user(username, email, os.urandom(12).hex())
            login_user(new_user, remember=True)

        flash(f'Logged in successfully as {username}!', category='success')
        return redirect(url_for('views.home'))

    except Exception as e:
        flash(f'Google login failed: {str(e)}', category='error')
        return redirect(url_for('auth.sign_in_up'))

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'logout':
            logout_user()
            flash('Logged out successfully.', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Still logged in.', category='info')
            return redirect(url_for('views.home'))

    return render_template('logout.html')


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form.get('Username')
        email = request.form.get('Email')
        user = User.query.filter_by(email=email).first()
        # Feature incomplete
    flash('Unable to reset password. Please try again later.', category='error')
    return render_template('sign_in_up.html')
    