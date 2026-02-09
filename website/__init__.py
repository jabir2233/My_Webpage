from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(dotenv_path='instance/.env')

db = SQLAlchemy()
oauth = OAuth()
DB_NAME = "database.db"
GMAIL_USER = os.environ.get('GMAIL_USER')
GMAIL_PASS = os.environ.get('GMAIL_PASS')
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
BREVO_API_KEY = os.environ.get('BREVO_API_KEY')

def create_app():
    app = Flask(__name__)

    # Secret key for sessions
    app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'secret key')

    # Database URL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{DB_NAME}'
    )

    # Fix old postgres scheme if present
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace(
            "postgres://", "postgresql://", 1
        )

    # Engine options to prevent SSL & connection errors on Render
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True,      # reconnect dead connections
        "pool_recycle": 280         # refresh before Render closes idle connections
    }

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PREFERRED_URL_SCHEME'] = 'https'

    # Initialize database
    db.init_app(app)

    # Initialize OAuth
    oauth.init_app(app)

    # Register OAuth providers
    register_oauth_providers(oauth)

    from .views import views as views_blueprint
    from .auth import auth as auth_blueprint

    app.register_blueprint(views_blueprint, url_prefix='/')
    app.register_blueprint(auth_blueprint, url_prefix='/')

    from .models import User, Note
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.sign_in_up'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.route('/clear_database_123')
    def clear_database():
        db.drop_all()
        db.create_all()
        return 'Database cleared and tables recreated!'

    @app.route('/view_database_123')
    def view_database():
        users = User.query.all()
        notes = Note.query.all()

        user_data = [{"id": user.id, "username": user.username, "password": user.password, "email": user.email} for user in users]

        note_data = [{"id": note.id, "data": note.data, "user_id": note.user_id} for note in notes]

        return jsonify({"users": user_data, "notes": note_data})

    return app

def create_database(app):
    if not os.path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database Successfully!')

def register_oauth_providers(oauth):
    # Register Google OAuth provider
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'},
    )

    # Register other OAuth providers here, e.g., Facebook
    # oauth.register(
    #     name='facebook',
    #     client_id=os.getenv('FACEBOOK_CLIENT_ID'),
    #     client_secret=os.getenv('FACEBOOK_CLIENT_SECRET'),
    #     access_token_url='https://graph.facebook.com/v10.0/oauth/access_token',
    #     authorize_url='https://www.facebook.com/v10.0/dialog/oauth',
    #     userinfo_endpoint='https://graph.facebook.com/me?fields=id,name,email',
    #     client_kwargs={'scope': 'email'},
    # )

