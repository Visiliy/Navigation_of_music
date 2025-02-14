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
import datetime

#
import numpy as np
import pyaudio
input()

differences = []
highs = []

NOTE_MIN = 60       # C4
NOTE_MAX = 69       # A4
FSAMP = 40000       # Sampling frequency in Hz
FRAME_SIZE = 2048   # How many samples per frame?
FRAMES_PER_FFT = 16 # FFT takes average across how many frames?

######################################################################
# Derived quantities from constants above. Note that as
# SAMPLES_PER_FFT goes up, the frequency step size decreases (so
# resolution increases); however, it will incur more delay to process
# new sounds.

SAMPLES_PER_FFT = FRAME_SIZE * FRAMES_PER_FFT
FREQ_STEP = float(FSAMP) / SAMPLES_PER_FFT

######################################################################
# For printing out notes

NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()

######################################################################
# These three functions are based upon this very useful webpage:
# https://newt.phys.unsw.edu.au/jw/notes.html

def freq_to_number(f): return 69 + 12 * np.log2(f / 440.0)
def number_to_freq(n): return 440 * 2.0**((n - 69) / 12.0)
def note_name(n): return NOTE_NAMES[n % 12] + str(n/12 - 1)

######################################################################
# Ok, ready to go now.

# Get min/max index within FFT of notes we care about.
# See docs for numpy.rfftfreq()
def note_to_fftbin(n): return number_to_freq(n)/FREQ_STEP
imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))

# Allocate space to run an FFT.
buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
num_frames = 0

# Initialize audio
stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                channels=1,
                                rate=FSAMP,
                                input=True,
                                frames_per_buffer=FRAME_SIZE)

stream.start_stream()

# Create Hanning window function
window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))

# Print initial text
print('sampling at', FSAMP, 'Hz with max resolution of', FREQ_STEP, 'Hz')
print()
last_note_name = 'asdjkhkdsj'

# As long as we are getting data:
while stream.is_active():

    # Shift the buffer down and new data in
    buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
    buf[-FRAME_SIZE:] = np.fromstring(stream.read(FRAME_SIZE), np.int16)

    # Run the FFT on the windowed buffer
    fft = np.fft.rfft(buf * window)

    # Get frequency of maximum response in range
    freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP

    # Get note number and nearest note
    n = freq_to_number(freq)
    n0 = int(round(n))

    # Console output once we have a full buffer
    num_frames += 1

    if num_frames >= FRAMES_PER_FFT:
        note = list(note_name(n0).split('.'))[0]
        print(note)
        if last_note_name != note:
            highs.append(note)
        last_note_name = note
        if note == 'B3':
            break

print(highs)
#


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
    nickname = db.Column(db.String())
    password = db.Column(db.String())
    favoritemusic = db.Column(db.Text())
    musicalhistory = db.Column(db.Text())

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
    print("OK_555")
    music_list = db.session.query(Music).all()
    print("OK_552")
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
    

def dp(AUDIO_FILE):
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
        print(pattern)
        ans = read_music(pattern)
        return ans
    except:
        return False


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
            name=req[0],
            nickname=req[1],
            password=generate_password_hash(req[2]),
            favoritemusic=json.dumps([]),
            musicalhistory=json.dumps([]),
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
        args = dict(request.args)
        print(args)
        error = False
        content = request.files["audio"].read()
        AUDIO_FILE = f"media_files/audioToSave{randrange(1, 100000000)}.wav"
        with open(AUDIO_FILE, "wb") as fh:
            fh.write(content)
        ans = dp(AUDIO_FILE)
        if ans is not False:
            array = [1]
            current_datetime = datetime.datetime.now()
            current_year = current_datetime.year
            current_month = current_datetime.month
            current_day = current_datetime.day
            str_format = f"{current_day}:{current_month}:{current_year}"
            array.append(str_format)
            for i in ans:
                array.append(i[1])
            user = Users.query.filter_by(nickname=args["nickname"]).first()
            res = json.loads(user.musicalhistory)
            res.append(array)
            user.musicalhistory = json.dumps(res)
            db.session.commit()

            os.remove(AUDIO_FILE)
        else:
            print(f"Exception")
            error = True
        if not error:
            print("OK")
            return jsonify(ans, 200)
        print("NO")
        return jsonify([(0, "ERROR")], 200)
    except:
        print("NO NO")
        return jsonify("ERROR", 200)


@app.route("/favorite_music", methods=["GET"])
def favorite_music():
    try:
        args = dict(request.args)
        user = Users.query.filter_by(nickname=args["nickname"]).first()
        res = json.loads(user.favoritemusic)
        if len(res) == 0:
            return jsonify([[1, "Пусто"]], 200)
        return jsonify(res, 200)
    except:
        return jsonify([[0, "error"]], 200)


@app.route("/musical_history", methods=["GET"])
def musical_history():
    try:
        args = dict(request.args)
        user = Users.query.filter_by(nickname=args["nickname"]).first()
        res = json.loads(user.musicalhistory)
        if len(res) == 0:
            return jsonify([[1, "Пусто"]], 200)
        return jsonify(res[::-1], 200)
    except:
        return jsonify([[0, "error"]], 200)
    

@app.route("/record_favorite_music", methods=["GET"])
def record_favorite_music():
    try:
        args = dict(request.args)
        user = Users.query.filter_by(nickname=args["nickname"]).first()
        res = json.loads(user.favoritemusic)
        if len(res) == 0:
            res.append([1, "Музыкальные произведения", args["music"]])
        elif args["music"] not in res[0]:
            res[0].append(args["music"])
        user.favoritemusic = json.dumps(res)
        db.session.commit()
        return jsonify("OK", 200)
    except:
        return jsonify("NO", 200)


def main():
    # with app.app_context():
    #     db.create_all()
    #     db.create_all(bind='FavoriteMusic')
    # users = Users(name="name", nickname="nickname", password="password")
    # db.session.add(users)
    # db.session.flush()
    # db.session.commit()
    # print(Users.query.filter_by(nickname="nickname").first())
    app.run(port=8070)


if __name__ == "__main__":
    main()


# python main.py
