from flask import *
from flask_cors import CORS
from random import randrange

app = Flask(__name__)
CORS(app)


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
    app.run(port=8070)


if __name__ == "__main__":
    main()


# python main.py
