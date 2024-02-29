from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Vaccinationcenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    location = db.Column(db.String(150)) 
    working_hours = db.Column(db.String(2))  
    dosage = db.Column(db.Integer)
    slots_booked = db.Column(db.Integer, default=10)
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))  
    role = db.Column(db.String(4), default="user")  


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    center_id = db.Column(db.Integer, db.ForeignKey('vaccinationcenter.id')) 
    booking_date = db.Column(db.Date, default=func.now()) 
    user = db.relationship('User', backref='bookings')
    center = db.relationship('Vaccinationcenter', backref='bookings')




