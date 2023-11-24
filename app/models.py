from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon_name = db.Column(db.String(45), nullable=False)
    ability_name = db.Column(db.String(45), nullable=False)
    base_experience = db.Column(db.Integer, nullable=False)
    front_shiny = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    bio = db.Column(db.String(300))

    pokemon_collection = db.relationship('Pokemon', backref='user', lazy=True)

    # New fields for tracking wins and losses
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
