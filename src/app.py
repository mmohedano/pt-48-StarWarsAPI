"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import json
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Favorites

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.route('/user', methods=['GET'])
def get_users():
    
    users = User.query.all()
    if users == []:
        
        return jsonify({"msg": "No users"}), 404 
                         
    result = list(map(lambda user: user.serialize(), users))
    return jsonify(result), 200


@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    body = json.loads(request.data) 
    favorites = Favorites.query.filter_by(user_id = body["user_id"]).all()
    if favorites == []:
        
        return jsonify({"msg": "No favorites"}), 404 
                        
    result = list(map(lambda favorite: favorite.serialize(), favorites)) 
    return jsonify(result), 200


@app.route('/user/<int:idUser>', methods=['GET', 'DELETE'])
def get_id_user(idUser):
    id_user = User.query.filter_by(id = idUser).first() 
    if id_user is None: 
        return jsonify({"msg": "User doesn't exists"}), 404
    if request.method == "GET": 
        return jsonify(id_user.serialize()), 200 
    if request.method == "DELETE":
        db.session.delete(id_user)
        db.session.commit()
        return jsonify({"msg": "User deleted"}), 200
     

@app.route('/user', methods=['POST'])
def add_user():
    body = json.loads(request.data) 
    new_user = User.query.filter_by(email = body["email"]).first() 
    if new_user is None:
        new_user = User(
            
            email = body["email"],
            password = body["password"],
            name = body["name"],
            
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User created"}), 200
    return jsonify({"msg": "User already exists"}), 404



@app.route('/people', methods=['GET'])
def get_people():
    
    people = People.query.all()
    if people == []:
        
        return jsonify({"msg": "No people"}), 404 
                         
    result = list(map(lambda person: person.serialize(), people)) 
    return jsonify(result), 200

        
@app.route('/people/<int:idPerson>', methods=['GET', 'DELETE'])
def get_id_people(idPerson):
    id_person = People.query.filter_by(id=idPerson).first() 
    if id_person is None: 
        return jsonify({"msg": "Person doesn't exist"}), 404
    if request.method == "GET": 
        return jsonify(id_person.serialize()), 200 
    if request.method == "DELETE":
        db.session.delete(id_person)
        db.session.commit()
        return jsonify({"msg": "Person deleted"}), 200 

@app.route('/people', methods=['POST'])
def add_people():
    body = json.loads(request.data) 
    new_person = Person.query.filter_by(name = body["name"]).first() 
    if new_person is None: 
        new_person = People(
            
            name = body["name"],
            description = body["description"]
        )
        db.session.add(new_person)
        db.session.commit() 
        return jsonify({"msg": "Person created"}), 200
    return jsonify({"msg": "Person already exists"}), 404



@app.route('/planets', methods=['GET'])
def get_planets():
    
    planets = Planet.query.all()
    if planets == []:
       
        return jsonify({"msg": "No planets"}), 404 
                         
    result = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(result), 200

 
@app.route('/planets/<int:idPlaneta>', methods=['GET', 'DELETE'])
def get_id_planets(idPlanet):
    id_planet = Planet.query.filter_by(id=idPlanet).first() 
    if id_planet is None: 
        return jsonify({"msg": "Planet doesn't exist"}), 404
    if request.method == "GET": 
        return jsonify(id_planet.serialize()), 200 
    if request.method == "DELETE":
        db.session.delete(id_planet)
        db.session.commit()
        return jsonify({"msg": "Planet deleted"}), 200 
    

@app.route('/planets', methods=['POST'])
def add_planet():
    body = json.loads(request.data) 
    new_planet = Planet.query.filter_by(name = body["name"]).first() 
    if new_planet is None: 
        new_planet = Planet(
           
            name = body["name"],
            description = body["description"]
        )
        db.session.add(new_planet)
        db.session.commit() 
        return jsonify({"msg": "Planet created"}), 200
    return jsonify({"msg": "Planet already exists"}), 404


@app.route('/favorites', methods=['GET'])
def get_favorites():
    
    favorites = Favorites.query.all()
    if favorites == []:
        
        return jsonify({"msg": "No favorites"}), 404 
                         
    result = list(map(lambda favorite: favorite.serialize(), favorites))
    return jsonify(result), 200

@app.route('/favorites', methods=['POST'])
def add_favorites():
    body = json.loads(request.data) 
    new_favorite = Favorites(
       
        user_id = body["user_id"], 
        planet_id = body["planet_id"],
        people_id = body["people_id"]
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite created"}), 200