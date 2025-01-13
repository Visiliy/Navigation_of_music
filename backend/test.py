import json
from main import Music
from difflib import SequenceMatcher
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
        return [(0, "ничего не найдено")]


def write_music():
    name = "Гимн России"
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


def pat():
    pattern = "Широкий простор для мечты и для жизни".split()
    for i in range(len(pattern)):
        pattern[i] = clear_word(pattern[i])
    ans = read_music(pattern)
    print("Название песни:", ans[0][1])
    print("Возможно, вы искали это:")
    for i in range(1, len(ans)):
        print(f"    {ans[i][1]}")


def get_misic_list():
    music_list = db.session.query(Music).all()
    for music in music_list:
        print(music.id, music.name)


def main():
    with app.app_context():
        # db.create_all()
        # get_misic_list()
        flag = False
        if flag:
            write_music()
        else:
            pat()
            # user = Music.query.get(5)
            # print(json.loads(user.text), user.name)
            # user.name = 'День Победы'
            # db.session.commit()
        print("OK")


if __name__ == "__main__":
    main()
    # python test.py
