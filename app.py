from flask import Flask, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    passhash = db.Column(db.String(512), nullable = False)
    name = db.Column(db.String(50), nullable = False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.passhash, password)
    
    #relationship
    carts = db.relationship('Mybooks', backref='User', lazy=True)
    feedbacks = db.relationship('Feedback', backref='User', lazy=True)

class Book(db.Model):
    __tablename__ = "Book"
    id = db.Column(db.Integer, primary_key = True)
    book_name = db.Column(db.String(20), nullable = False)
    section_id = db.Column(db.Integer, db.ForeignKey('Section.id'), nullable = False)
    content = db.Column(db.String(20), nullable = False)
    author = db.Column(db.String(20), nullable = False)
    pdf_path = db.Column(db.String(255), nullable = False)

    #relationship
    carts = db.relationship('Mybooks', backref='Book', lazy=True)

class Section(db.Model):
    __tablename__ = "Section"
    id = db.Column(db.Integer, primary_key = True)
    section_name = db.Column(db.String(50), nullable = False)
    date_created = db.Column(db.Date, nullable = False)
    description = db.Column(db.String(50), nullable = False)

    # relationship
    books = db.relationship('Book', backref='Section', lazy=True)

class Mybooks(db.Model):
    __tablename__ = "Mybooks"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey('Book.id'), nullable = False)
    issue_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default="Pending")

class Feedback(db.Model):
    __tablename__ = "Feedback"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey('Book.id'), nullable = False)
    feedback = db.Column(db.String(200))