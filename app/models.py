"""
The database model

"""
from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'

    UserID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(100))
    LastName = db.Column(db.String(100))
    Email = db.Column(db.String(100), unique=True)
    ProfileImage = db.Column(db.String(255))

    products = db.relationship('Product', backref='seller', lazy=True)
    sent_messages = db.relationship('Message', foreign_keys='Message.SenderID', backref='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.ReceiverID', backref='receiver', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    addresses = db.relationship('Address', backref='user', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'

    ProductID = db.Column(db.Integer, primary_key=True)
    SellerID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
    CategoryID = db.Column(db.Integer, db.ForeignKey('categories.CategoryID'))
    ProductName = db.Column(db.String(100))
    ProductColor = db.Column(db.String(50))
    Description = db.Column(db.String(255))
    Price = db.Column(db.Float)
    Condition = db.Column(db.String(50))
    DatePosted = db.Column(db.DateTime, default=datetime.utcnow)
    IsSold = db.Column(db.Boolean, default=False)

    images = db.relationship('Image', backref='product', lazy=True)

    __table_args__ = (
        CheckConstraint(Condition.in_(['New', 'Used', 'Refurbished'])),
    )

class Category(db.Model):
    __tablename__ = 'categories'

    CategoryID = db.Column(db.Integer, primary_key=True)
    CategoryName = db.Column(db.String(100))

    products = db.relationship('Product', backref='category', lazy=True)

class Image(db.Model):
    __tablename__ = 'images'

    ImageID = db.Column(db.Integer, primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('products.ProductID'))
    ImageURL = db.Column(db.String(255))

class Message(db.Model):
    __tablename__ = 'messages'

    MessageID = db.Column(db.Integer, primary_key=True)
    SenderID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
    ReceiverID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
    MessageText = db.Column(db.String(255))
    MessageDate = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    __tablename__ = 'notifications'

    NotificationID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
    NotificationText = db.Column(db.String(255))
    NotificationDate = db.Column(db.DateTime, default=datetime.utcnow)
    IsRead = db.Column(db.Boolean)

class Address(db.Model):
    __tablename__ = 'addresses'

    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), primary_key=True)
    Street = db.Column(db.String(100), primary_key=True)
    City = db.Column(db.String(100), primary_key=True)
    State = db.Column(db.String(100), primary_key=True)
    ZipCode = db.Column(db.String(20), primary_key=True)
    Country = db.Column(db.String(100))

    __table_args__ = (
        UniqueConstraint('UserID', 'Street', 'City', 'State', 'ZipCode'),
    )
