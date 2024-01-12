from flask import Flask, make_response, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
from models import db, Toys, Users
from flask_cors import CORS
from dotenv import dotenv_values
from flask_bcrypt import Bcrypt
config = dotenv_values(".env")

app = Flask(__name__)
app.secret_key = config['FLASK_SECRET_KEY']
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "toy backend"

    
@app.get('/check_session')
def check_session():
    user = db.session.get(Users, session.get('user_id'))
    print(f'check session {session.get("user_id")}')
    if user:
        return user.to_dict(rules=['-password_hash']), 200
    else:
        return {"message": "No user logged in"}, 401

@app.get('/toys/')
def get_toys():
    #python object
    toys = Toys.query.all()
    #convert each nested python object into json
    return [toy.to_dict() for toy in toys]

@app.get('/users/<int:id>/toys')
def get_toys_for_user(id):
    user = db.session.get(Users, id)
    if not user:
        return {"error":"user not found"}, 404
    return [d.to_dict() for d in user.toys], 200

@app.get('/toys/<int:id>')
def get_toys_by_id(id):
    toy = Toys.query.filter_by(id=id).first()
    return toy.to_dict()

@app.patch('/toys/<int:id>')
def patch_toys(id):
    toy = db.session.get(Toys, id)
    data = request.json
    for key in data:
        setattr(toy, key, data[key])
        # setattr(object, name, value)
    db.session.add(toy)
    db.session.commit()
    # return the new toy with updated attributes
    return toy.to_dict()

@app.delete('/toys/<int:id>')
def delete_toys(id):
    toy = db.session.get(Toys, id)
    db.session.delete(toy)
    db.session.commit()
    return {}

@app.post('/toys')
def post_toys():
    data = request.json
    new_toy = Toys(name=data['name'], image=data['image'], likes=0, user_id=session.get("user_id"))
    db.session.add(new_toy)
    db.session.commit()
    return new_toy.to_dict()

@app.delete('/logout')
def logout():
    session.pop('user_id')
    return {"message": "Logged out"}, 200

@app.post('/login')
def login():
    data = request.json
    user = Users.query.filter(Users.name == data.get('name')).first()

    if user and bcrypt.check_password_hash(user.password_hash, data.get('password')):
        session["user_id"] = user.id
        print("success")
        return user.to_dict(), 200
    else:
        return { "error": "Invalid username or password"}, 401

if __name__ == "__main__":
    app.run(port=5555, debug=True)