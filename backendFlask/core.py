from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from sqlalchemy import UniqueConstraint
import requests
from producer import publish

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

@core.route('/api/houses')
def index():
    return jsonify(House.query.all())

@core.route('/api/houses/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://localhost:5002/api/checker')
    json = req.json()

    try:
        # Create a new houseChecker with the checker id and the house id
        houseChecker = HouseChecker(checker_id=json['id'], house_id=id)
        # Save the new houseChecker
        db.session.add(houseChecker)
        db.session.commit()
        # Publish a new message to the RabbitMQ
        publish('house_liked', id)
    except:
        abort(400, 'You already liked this house')
    
    return jsonify({
        'message': 'success'
    })

@core.route('/api/houses/<int:id>/check', methods=['POST'])
def check(id):
    req = requests.get('http://localhost:5002/api/checker')
    json = req.json()

    try:
        # Create a new houseChecker with the checker id and the house id
        houseChecker = HouseChecker(checker_id=json['id'], house_id=id)
        # Save the new houseChecker
        db.session.add(houseChecker)
        db.session.commit()
        # Publish a new message to the RabbitMQ
        publish('house_checked', id)
    except:
        abort(400, 'You already checked this house')
    
    return jsonify({
        'message': 'success'
    })


if __name__ == '__main__':
    core.run(debug=True, host='0.0.0.0', port=5001)