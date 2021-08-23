
from threading import Event
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/ey'
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b3x2mzn3vgxhrr12:kk1wi098ezdx4bdb@tvcpw8tpu4jvgnnq.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/pwjh6mzn4jk2lehc'

db = SQLAlchemy(app)


 #----DATABASE START----#
class Mail_db(db.Model):
    
    Index = db.Column(db.Integer, primary_key=True)
    Country = db.Column(db.String(80), nullable=False)
    Company = db.Column(db.String(12), nullable=False)
    Date = db.Column(db.String(30), nullable=False)
    City = db.Column(db.String(50), nullable=False)
    Prediction = db.Column(db.String(50), nullable=False)
    Advice = db.Column(db.String(1000), nullable=False)
    Info = db.Column(db.String(100), nullable=False)
    Travellers = db.Column(db.String(50), nullable=False)
    Severity = db.Column(db.String(10), nullable=False)
    Distance = db.Column(db.String(10), nullable=False)
    Subject = db.Column(db.String(200), nullable=False)
    Event = db.Column(db.String(200), nullable=True)
    
    
    
class Risk_rating(db.Model):
    
    LOCATION = db.Column(db.Integer, primary_key=True)  
    
 #----DATABASE END----#


