from flask import *
from flask_cors import CORS
from random import randrange
from flask_sqlalchemy import SQLAlchemy

from services import UserAuthorization

app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "5457fae2a71f9331bf4bf3dd6813f90abeb33839f4608755ce301b9321c671791673817685w47uer6uuu"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)
CORS(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    nickname = db.Column(db.String(30))
    password = db.Column(db.String())

    def __repr__(self):
        return f"<users {self.id}>"


@app.route("/login_user", methods=["POST"])
def login_user():
    try:
        req = request.get_json()
        print(req)
        return jsonify("Ok", 200)
    except:
        return "No"


@app.route("/user_registration", methods=["POST"])
def user_registration():
    try:
        req = request.get_json()
        print(req)
        return jsonify("Ok2", 200)
    except:
        return "No"


@app.route("/get_music", methods=["GET"])
def get_music():
    return jsonify("hello", 200)


@app.route("/get_music", methods=["POST"])
def get_music2():
    try:
        content = request.files["audio"].read()
        with open(f"media_files/audioToSave{randrange(1, 100000000)}.mp3", "wb") as fh:
            fh.write(content)
        return jsonify("OK", 200)
    except:
        return jsonify("ERROR", 200)


def main():
    # with app.app_context():
    #     db.create_all()
    app.run(port=8070)


if __name__ == "__main__":
    main()


# python main.py
