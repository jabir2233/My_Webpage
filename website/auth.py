from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, oauth
from flask_login import login_user, login_required, logout_user, current_user
from website.utils.send_mail import send_email
from website.utils.otp import generate_otp
import threading
import os

auth = Blueprint('auth', __name__)

def create_user(username, email, password):
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user


@auth.route('/sign_in_up', methods=['GET', 'POST'])
def sign_in_up():
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

     # Handle form submission
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        username = request.form.get('Username', '').strip()
        email = request.form.get('Email', '').strip()
        password = request.form.get('Password', '').strip()
        confirm_password = request.form.get('CPassword', '').strip()

        if form_type == 'login':
            if not email or not password:
                flash('Email and password are required.', category='error')
                return redirect(url_for('auth.sign_in_up'))

            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully.', category='success')
                return redirect(url_for('views.home'))
            flash('Invalid email or password.', category='error')

        elif form_type == 'signup':
            if not username or not email or not password or not confirm_password:
                flash('All fields are required to sign up.', category='error')
            elif User.query.filter_by(email=email).first():
                flash('Email already exists.', category='error')
            elif len(username) < 3:
                flash('Username must be at least 3 characters.', category='error')
            elif password != confirm_password:
                flash('Passwords do not match.', category='error')
            else:
                #Generate OTP
                otp = generate_otp()
                #store form data and email temporarily
                session['pending_user'] = {
                    'username': username,
                    'email': email,
                    'password': password,
                    'otp': otp
                }

                #Send OTP to user's email in a separate thread
                threading.Thread(
                    target=send_email,
                    args=(email, otp),
                    daemon=True
                ).start()
                
                flash('An OTP has been sent to your email. Please verify to complete registration.', category='success')

                return redirect(url_for('auth.verify_email'))
                

    return render_template('sign_in_up.html')

@auth.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    pending = session.get('pending_user')

    if not pending:
        flash("No verification in progress.", "error")
        return redirect(url_for('auth.sign_in_up'))

    if request.method == 'POST':
        user_otp = request.form.get('otp')

        if user_otp == pending['otp']:

            # Create user now
            new_user = create_user(
                pending['username'],
                pending['email'],
                pending['password']
            )

            session.pop('pending_user')

            login_user(new_user, remember=True)
            flash("Your email has been verified!", "success")
            return redirect(url_for('views.home'))

        else:
            flash("Incorrect OTP. Try again.", "error")

    return render_template('verify.html', email=pending['email'])


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
    