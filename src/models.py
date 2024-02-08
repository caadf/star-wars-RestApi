from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User (db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    favorites_people = db.relationship('Favorite_People', backref = 'user')
    favorites_planet = db.relationship('Favorite_Planet', backref = 'user')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        } 

class People (db.Model):
    __tablename__ = 'peoples'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(120), nullable=False)
    hair_color = db.Column(db.String(120), nullable=False)
    favorite_p = db.relationship('Favorite_People', backref = 'people')

    def serialize(self):
        return {
            "id": self.id,
            "gender": self.gender,
            "hair_color": self.hair_color 
        } 

class Planet (db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    climate = db.Column(db.String(120), nullable=False)
    gravity = db.Column(db.String(120), nullable=False)
    favorite_pla = db.relationship('Favorite_Planet', backref = 'planet')

    def serialize(self):
        return {
            "id": self.id,
            "climate": self.climate,
            "gravity": self.gravity
        } 


class Favorite_People (db.Model):
    __tablename__ = 'favorites_peoples'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('peoples.id'))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id
        } 

class Favorite_Planet (db.Model):
    __tablename__ = 'favorites_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        } 
