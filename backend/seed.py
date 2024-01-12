from app import app
from models import Toys, Users, db
import json
from flask_bcrypt import Bcrypt
import random

if __name__ == '__main__':
    with app.app_context():
        bcrypt = Bcrypt(app)
        data = {}
        with open ("db.json") as f:
            data = json.load(f)
        Toys.query.delete()
        Users.query.delete()

        toy_list = []
        for toy in data["toys"]:
            t = Toys(name=toy.get('name'), image=toy.get('image'), likes=toy.get('likes'), user_id=toy.get('user_id'))
            toy_list.append(t)

        db.session.add_all(toy_list)
        db.session.commit()

        user_list = []
        for user in data["users"]:
            password_hash = bcrypt.generate_password_hash(user.get('password_hash'))
            u = Users(
                name=user.get("name"),
                password_hash=password_hash,
            )
            user_list.append(u)

        db.session.add_all(user_list)
        db.session.commit()