from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import string, datetime

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)

class Toys(db.Model, SerializerMixin):
    __tablename__ = "toy_table"
    serialize_rules = ['-user']
   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    likes = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))
    user = db.relationship('Users', back_populates='toys')

class Users(db.Model, SerializerMixin):
    __tablename__ = "user_table"
    serialize_rules = ['-toys.user']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password_hash = db.Column(db.String)
    
    toys = db.relationship('Toys', back_populates='user')


