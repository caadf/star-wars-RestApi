"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite_People, Favorite_Planet
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
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


""" GET POST PUT DELETE EN EL EJERCICIO
 """

""" PEOPLE """

@app.route('/people', methods=['GET'])
def handle_all_people():
    people_all = People.query.all()
    people_all =  list(map(lambda people_all: people_all.serialize(), people_all))

    return jsonify(people_all), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    people = People.query.filter_by(id = people_id).first()
    result = people.serialize()
    return jsonify(result), 200

""" PLANET """

@app.route('/planets', methods=['GET'])
def handle_all_planet():
    planet_all = Planet.query.all()
    planet_all =  list(map(lambda planet_all: planet_all.serialize(), planet_all))

    return jsonify(planet_all), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    planet = Planet.query.filter_by(id = planet_id).first()
    result = planet.serialize()

    return jsonify(result), 200

""" USER """

@app.route('/user', methods=['GET'])
def handle_all_user():
    user_all = User.query.all()
    user_all =  list(map(lambda user_all: user_all.serialize(), user_all))

    return jsonify(user_all), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    user = User.query.filter_by(id = user_id).first()
    result = user.serialize()

    return jsonify(result), 200

@app.route('/user/favorites', methods=['GET'])
def user_favorites():
    
    user_id=1
    favorite_planets = Favorite_Planet.query.filter_by(user_id=user_id)  
    favorite_peoples = Favorite_People.query.filter_by(user_id= user_id) 
    favorite = favorite_planets + favorite_peoples
    return jsonify(favorite), 200
    

    
""" POST PLANET """
@app.route('/planets', methods=['POST'])
def create_planet():
    datos = request.get_json()

    climate = request.json.get('climate')
    gravity = request.json.get('gravity')
  
    new_planet = Planet()
    new_planet.climate = climate
    new_planet.gravity = gravity
    
    db.session.add(new_planet) 
    db.session.commit()

    return jsonify(new_planet.serialize()), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
 
    user_id=1
    favorite_planets = Favorite_Planet()  
    favorite_planets.user_id=user_id
    favorite_planets.planet_id=planet_id

    db.session.add(favorite_planets) 
    db.session.commit()
    return jsonify(favorite_planets.serialize), 200
  

""" POST PEOPLE """

@app.route('/people', methods=['POST'])
def create_people():
    datos = request.get_json()

    gender = request.json.get('gender')
    hair_color = request.json.get('hair_color')
  
    new_people = People()
    new_people.gender = gender
    new_people.hair_color = hair_color
    
    db.session.add(new_people) 
    db.session.commit()

    return jsonify(new_people.serialize()), 201

@app.route('/favorite/people/<int:people_id> ', methods=['POST'])
def add_favorite_people(people_id):
 
    user_id=1
    favorite_people = Favorite_People()  
    favorite_people.user_id=user_id
    favorite_people.people_id=people_id

    db.session.add(favorite_people) 
    db.session.commit()
    return jsonify(favorite_people.serialize), 200
  
""" DELETE """
@app.route('/favorite/planet/<int:planet_id> ', methods=['DELETE'])
def delete_planet(planet_id):
    

    planet = Favorite_Planet.query.get(planet_id)
    
    if not planet: return jsonify({"msg": "Planet doesn't exist!"}), 404
    
    db.session.delete(planet)
    db.session.commit()
    
    return jsonify({"msg": "Planet was deleted!"}), 200

@app.route('/favorite/planet/<int:people_id> ', methods=['DELETE'])
def delete_planet( people_id):
    
    people = Favorite_People.query.get(people_id)
    
    if not people: return jsonify({"msg": "People doesn't exist!"}), 404
    
    db.session.delete(people)
    db.session.commit()
    
    return jsonify({"msg": "People was deleted!"}), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
