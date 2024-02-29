from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from sqlalchemy import UniqueConstraint

# Create a new Flask application
core = Flask(__name__)

# Enable CORS
CORS(core)

# config SQLAlchemy
core.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://microservice:microservice@db/core'

# Initialize the database
db = SQLAlchemy(core)

@dataclass
class House(db.Model):
    id: int
    name: str
    image: str
    description: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(150))
    image = db.Column(db.String(150))
    description = db.Column(db.String(150))

@dataclass
class HouseChecker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checker_id = db.Column(db.Integer)
    house_id = db.Column(db.Integer)

    UniqueConstraint('checker_id', 'house_id', name='checker_house_unique')

@core.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    core.run(debug=True, host='0.0.0.0', port=5001)