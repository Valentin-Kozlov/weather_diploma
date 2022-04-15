from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= "mysql+mysqldb://root:root@192.168.146.162:3306/test_flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Date_table(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    weather_state_name = db.Column(db.String(20), nullable=True)
    wind_direction_compass = db.Column(db.String(20), nullable=True) 
    created = db.Column(db.String(40), nullable=True) 
    applicable_date = db.Column(db.DateTime(20), nullable=False)
    min_temp = db.Column(db.String(20), nullable=True) 
    max_temp = db.Column(db.String(20), nullable=True) 
    the_temp = db.Column(db.String(20), nullable=True)
    
db.create_all()