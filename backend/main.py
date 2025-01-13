from flask import *
from flask_cors import CORS
from random import randrange
from difflib import SequenceMatcher
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
import json
import os

import librosa
import numpy as np


app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "5457fae2a71f9331bf4bf3dd6813f90abeb33839f4608755ce301b9321c671791673817685w47uer6uuu"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_BINDS"] = {"music": "sqlite:///music.db"}
db = SQLAlchemy(app)
CORS(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10))
    nickname = db.Column(db.String(30))
    password = db.Column(db.String())

    def __repr__(self):
        return f"<users {self.id}>"


class Music(db.Model):

    __bind_key__ = "music"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String())
    text = db.Column(db.Text())

    def __repr__(self):
        return f"<users {self.id}>"


def clear_word(word):
    word = word.lower()
    word = word.strip(".")
    word = word.strip(",")
    word = word.strip("«")
    word = word.strip("»")
    word = word.strip("?")
    word = word.strip("!")
    return word


def read_music(pattern):
    max_value = 0
    hash_map = {}
    music_list = db.session.query(Music).all()
    for music in music_list:
        music_text = json.loads(music.text)
        count = 0
        for i in pattern:
            max_koeff = 0
            for word in music_text:
                matcher = SequenceMatcher(None, i, word)
                similarity = matcher.ratio()
                max_koeff = max(max_koeff, similarity)
            if max_koeff >= 0.7:
                count += 1
        max_value = max(max_value, count)
        if count > 0:
            hash_map[count] = music.name
    name_list = sorted(hash_map.items(), reverse=True, key=lambda x: x[0])
    if max_value > 0:
        return name_list[: min(len(name_list), 5)]
    else:
        return [(0, "Ничего не найдено")]


@app.route("/login_user", methods=["POST"])
def login_user():
    try:
        req = request.get_json()
        user = Users.query.filter_by(nickname=req[0]).first()
        if user:
            if check_password_hash(user.password, req[1]):
                return jsonify([True, True, user.name], 200)
            else:
                return jsonify([False, False, ""], 200)
        return jsonify([True, False, ""], 200)
    except:
        return jsonify([False, True, ""], 200)


@app.route("/user_registration", methods=["POST"])
def user_registration():
    try:
        req = request.get_json()
        if Users.query.filter_by(nickname=req[1]).first():
            return jsonify([False, False], 200)
        users = Users(
            name=req[0], nickname=req[1], password=generate_password_hash(req[2])
        )
        db.session.add(users)
        db.session.flush()
        db.session.commit()
        return jsonify([True, True], 200)
    except:
        return jsonify([False, True], 200)


@app.route("/get_music", methods=["GET"])
def get_music():
    return jsonify("hello", 200)


@app.route("/get_music", methods=["POST"])
def get_music2():
    try:
        error = False
        content = request.files["audio"].read()
        AUDIO_FILE = f"media_files/audioToSave{randrange(1, 100000000)}.wav"
        with open(AUDIO_FILE, "wb") as fh:
            fh.write(content)
        try:
            deepgram = DeepgramClient("50a062200dc80b224f63d15175a7b8bb6e10e395")

            with open(AUDIO_FILE, "rb") as file:
                buffer_data = file.read()

            payload: FileSource = {
                "buffer": buffer_data,
            }

            options = PrerecordedOptions(
                model="nova-2",
                smart_format=True,
                language="ru",
            )

            response = deepgram.listen.rest.v("1").transcribe_file(payload, options)
            pattern = json.loads(response.to_json(indent=4))["results"]["channels"][0][
                "alternatives"
            ][0]["transcript"]
            pattern = pattern.split()
            for i in range(len(pattern)):
                pattern[i] = clear_word(pattern[i])
            ans = read_music(pattern)
            print(pattern)
            os.remove(AUDIO_FILE)
        except Exception as e:
            print(f"Exception: {e}")
            error = True
        if not error:
            print("OK")
            return jsonify(ans, 200)
        print("NO")
        return jsonify([(0, "ERROR")], 200)
    except:
        print("NO NO")
        return jsonify("ERROR", 200)


def main():
    # with app.app_context():
    #     db.create_all()
    # db.create_all(bind='music')
    # users = Users(name="name", nickname="nickname", password="password")
    # db.session.add(users)
    # db.session.flush()
    # db.session.commit()
    # print(Users.query.filter_by(nickname="nickname").first())
    app.run(port=8070)


if __name__ == "__main__":
    main()


# python main.py
