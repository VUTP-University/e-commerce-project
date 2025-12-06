import uuid
from extensions import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(256), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    addresses = db.relationship('Address', back_populates='user', cascade='all, delete-orphan')

    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.username}>'

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.String(256), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(256), db.ForeignKey('users.id'), nullable=False)
    street = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    zip = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    user = db.relationship('User', back_populates='addresses')

    
    def __init__(self, user_id, street, city, zip, country):
        self.user_id = user_id
        self.street = street
        self.city = city
        self.zip = zip
        self.country = country