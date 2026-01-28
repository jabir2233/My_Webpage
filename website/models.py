from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime, timedelta

class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  data = db.Column(db.String(10000))
  date = db.Column(db.DateTime(timezone=True), default=func.now)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#Create a Pending User Class that inherits from db.model with Timeout
class PendingUser(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  otp = db.Column(db.String(6), nullable=False)
  otp_expiry = db.Column(db.DateTime, nullable=False)


# Create a User Class that inherits from db.model & UserMixin
class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20))
  email = db.Column(db.String(120), unique=True)
  password = db.Column(db.String(60))
  notes = db.relationship('Note')
