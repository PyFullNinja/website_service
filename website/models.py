from flask_login import UserMixin
from website import db
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column


class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.username}>"


class Services(db.Model, UserMixin):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("users.id", name="fk_services_user_id"), nullable=False)
    contact = db.Column(db.String(150), nullable=False)
    photos = db.relationship("Photos", backref="service", lazy=True)
    viewers = db.relationship("Views", backref="service", cascade="all, delete-orphan")
    views = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Service {self.service_name}>"


class Photos(db.Model, UserMixin):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)
    service_id = mapped_column(ForeignKey("services.id"))
    photo_url = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f"<Photo {self.photo_url}>"


class Views(db.Model, UserMixin):
    __tablename__ = "service_views"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)


class Logs(db.Model, UserMixin):
    __tablename__ = "logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) #пользователь
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #время
    category = db.Column(db.String(20), nullable=False) #категория
    action = db.Column(db.String(255), nullable=False) #действие 
    ip_address = db.Column(db.String(45), nullable=True) #ip
    user = db.relationship('Users', backref=db.backref('logs', lazy=True)) #пользователь

    def __repr__(self):
        return f"<Log {self.id}>"