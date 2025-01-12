from flask import *
from flask_cors import CORS
from random import randrange
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
app.config['SQLALCHEMY_BINDS'] = {
    'music': 'sqlite:///music.db'
}
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

    __bind_key__ = 'music'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String())
    text = db.Column(db.Text())

    def __repr__(self):
        return f"<users {self.id}>"


class Sound:
    def init(self, file):
        self.name = file

    def get_average_pitches(self):
        segment_length_ms = 0.01
        """
        Считывает аудиофайл, делит его на отрезки и вычисляет среднюю высоту тона для каждого.

        Args:
            audio_file: Путь к аудиофайлу.
            segment_length_ms: Длина отрезка в миллисекундах.

        Returns:
            Список средних высот тона для каждого отрезка (в герцах).  Возвращает None в случае ошибки.
        """
        try:
            y, sr = librosa.load(self.name)  # Загружаем аудио
            segment_length_samples = int(
                sr * segment_length_ms
            )  # Длина отрезка в семплах

            if segment_length_samples == 0:
                return None

            # num_segments = [y[i:i + segment_length_samples] for i in range(0, len(y), segment_length_samples)]

            pitches = []
            highs = []
            rythm = []
            j = 0
            e = 1
            for i in range(0, len(y), segment_length_samples):
                segment = y[i : i + segment_length_samples]
                # Используем librosa.yin для оценки высоты тона (более подходит для коротких отрезков)
                pitch = librosa.yin(segment, fmin=80, fmax=8000)  # Настраиваем частоты
                if (
                    pitch is not None
                ):  # Обрабатываем случаи, когда метод не может определить высоту тона
                    pitches.append(pitch)
                else:
                    pitches.append(
                        0.0
                    )  # Или другое значение для обозначения отсутствия тона.
                if j != 0:
                    if pitches[j - 1] != pitch:
                        highs.append(pitch)
                        e += 1
                    else:
                        rythm.append(e)
                        e = 1
                else:
                    highs.append(pitch)
                j += 1
            self.pitches = pitches
            return rythm

        except FileNotFoundError:
            print(f"Ошибка: Файл {self.name} не найден.")
            return None
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None


# Пример использования
# s = Sound('dddd.wav')
# print(s.get_average_pitches())


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

            print(
                json.loads(response.to_json(indent=4))["results"]["channels"][0][
                    "alternatives"
                ][0]["transcript"]
            )
            os.remove(AUDIO_FILE)
        except Exception as e:
            print(f"Exception: {e}")
            error = True
        if not error:
            print("OK")
            return jsonify("OK", 200)
        print("NO")
        return jsonify("ERROR", 200)
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
