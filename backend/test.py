import json
from main import Music
from main import db, app


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
            if i in music_text:
                count += 1
        max_value = max(max_value, count)
        if count > 0:
            hash_map[count] = music.name
    if max_value > 0:
        return hash_map[max_value]
    else:
        return "ничего не найдено"

def write_music():
    name = "Снежинка"
    text = ""
    with open("text.txt", "r", encoding="utf-8") as file:
        t = file.read().split()
        for word_index in range(len(t)):
            t[word_index] = clear_word(t[word_index])
        # print(t)
        text = json.dumps(t)
    music = Music(name=name, text=text)
    db.session.add(music)
    db.session.flush()
    db.session.commit()


def main():
    with app.app_context():
        # db.create_all()
        # write_music()
        pattern = "Исполнит вмиг мечту твою...".split()
        for i in range(len(pattern)):
            pattern[i] = clear_word(pattern[i])
        ans = read_music(pattern)
        print("Название песни:", ans)
        print("OK")


if __name__ == "__main__":
    main()
    # python test.py