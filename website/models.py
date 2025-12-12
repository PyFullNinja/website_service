from flask_login import UserMixin
from website import db

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
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("users.id", name="fk_services_user_id"), nullable=False)
    contact = db.Column(db.String(150), nullable=False)
    photos = db.relationship("Photos", backref="service", lazy=True)
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
