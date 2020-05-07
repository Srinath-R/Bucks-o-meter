from . import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

# class Card(db.Model):
#     card_no = db.Column(db.Integer, primary_key=True) 
#     bank = db.Column(db.String(1000))
#     balance  = db.Column(db.Integer, default = 0)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default = datetime.date.today())
    category = db.Column(db.String(100))
    amount = db.Column(db.Float) 
    note = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
