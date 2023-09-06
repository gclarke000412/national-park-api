from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, User, Park, ParkSchema, park_schema, parks_schema

api = Blueprint('api',__name__, url_prefix='/api')

# Create park
@api.route('/parks', methods = ['POST'])
@token_required
def create_park(current_user_token):
    park_name = request.json['park_name']
    state = request.json['state']
    founded = request.json['founded']
    popularity = request.json['popularity']
    beauty = request.json['beauty']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    park = Park(park_name,state,founded,popularity,beauty,user_token = user_token)

    db.session.add(park)
    db.session.commit()

    response = park_schema.dump(park)
    return jsonify(response)

# Retrieve park
@api.route('/parks', methods = ['GET'])
@token_required
def get_parks(current_user_token):
    owner = current_user_token.token
    parks = Park.query.filter_by(user_token = owner).all()
    response = parks_schema.dump(parks)
    return jsonify(response)

# Retrieve 1 park
@api.route('/parks/<id>', methods = ['GET'])
@token_required
def get_park(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        park = Park.query.get(id)
        response = park_schema.dump(park)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token required"}),401
    
#Update park
@api.route('/parks/<id>', methods = ['POST', 'PUT'])
@token_required
def update_park(current_user_token, id):
    park = Park.query.get(id)

    park.brand = request.json['brand']
    park.age = request.json['age']
    park.rating = request.json['rating']
    park.flavor = request.json['flavor']
    park.price = request.json['price']
    park.user_token = current_user_token.token

    db.session.commit()
    response = park_schema.dump(park)
    return jsonify(response)

#Delete park
@api.route('/parks/<id>', methods = ['DELETE'])
@token_required
def delete_park(current_user_token, id):
    park = Park.query.get(id)
    db.session.delete(park)
    db.session.commit()
    response = park_schema.dump(park)
    return jsonify(response)

