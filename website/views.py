import time
from flask import render_template, request, flash, redirect, url_for
from flask import Blueprint
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'logout':
            return redirect(url_for('auth.logout'))
        elif action == 'login':
            return redirect(url_for('auth.sign_in_up'))
            
    return render_template('home.html')

