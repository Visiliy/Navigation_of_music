import librosa
import numpy as np
import crepe
import pretty_midi

def frequency_to_note(frequency):
    """Определение названия ноты по частоте с помощью бинарного поиска"""
    if frequency <= 0:
        return None  # Некорректная частота

    note_names = [
        "C0", "C#0", "D0", "D#0", "E0", "F0", "F#0", "G0", "G#0", "A0", "A#0", "B0",
        "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1", "A1", "A#1", "B1",
        "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2",
        "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
        "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
        "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5",
        "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6",
        "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7", "G#7", "A7", "A#7", "B7",
        "C8", "C#8", "D8", "D#8", "E8", "F8", "F#8", "G8", "G#8", "A8", "A#8", "B8",
    ]

    frequencies = [
        16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87,
        32.70, 34.65, 36.71, 38.89, 41.20, 43.65, 46.25, 49.00, 51.91, 55.00, 58.27, 61.74,
        65.41, 69.30, 73.42, 77.78, 82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47,
        130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94,
        261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88,
        523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77,
        1046.50, 1108.73, 1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98, 1661.22, 1760.00, 1864.66, 1975.53,
        2093.00, 2217.46, 2349.32, 2489.02, 2637.02, 2793.83, 2959.96, 3135.96, 3322.44, 3520.00, 3729.31, 3951.07,
        4186.01, 4434.92, 4698.64, 4978.03, 5274.04, 5587.65, 5919.91, 6271.93, 6644.88, 7040.00, 7458.62, 7902.13,
    ]

    low = 0
    high = len(frequencies) - 1
    while low <= high:
        mid = (low + high) // 2
        if frequencies[mid] < frequency:
            low = mid + 1
        elif frequencies[mid] > frequency:
            high = mid - 1
        else:
            insertion_point = mid
            break
    insertion_point = low

    if insertion_point == 0:
        return note_names[0]
    elif insertion_point == len(frequencies):
        return note_names[-1]


    lower_index = insertion_point - 1
    higher_index = insertion_point

    lower_freq = frequencies[lower_index]
    higher_freq = frequencies[higher_index]

    distance_lower = frequency - lower_freq
    distance_higher = higher_freq - frequency

    if distance_lower <= distance_higher:
        return note_names[lower_index]
    else:
        return note_names[higher_index]


class Music_row():
    def __init__(self, file):
        self.file = file

    def load_and_preprocess(self):
        """Загружает аудио и выполняет предварительную обработку."""
        y, sr = librosa.load(self.file, sr=None)
        y = librosa.effects.trim(y)[0]
        y = librosa.util.normalize(y)
        self.y = y
        self.sr = sr

    def extract_pitch_with_crepe(self):
        """Извлекает высоту тона с помощью CREPE"""
        time, frequency, confidence, _ = crepe.predict(self.y, self.sr, viterbi=True, step_size=40)
        self.frequency = frequency
        self.confidence = confidence

    def filter_notes(self):
        """Фильтрация нот, избавление от помех"""
        self.segments = [0]
        last_note = frequency_to_note(self.frequency[0])
        extra = 'C0'
        extra_count = 0
        for i in range(1, len(self.frequency)):
            if self.confidence[i] >= 0.5:
                note_name = frequency_to_note(self.frequency[i])
                if note_name != last_note:
                    if extra == note_name:
                        extra_count += 1
                    else:
                        extra = note_name
                        extra_count = 1
                else:
                    extra_count = 0
                if extra_count == 10:
                    last_note = note_name
                    if self.segments[-1] != note_name:
                        self.segments.append(note_name)
        self.segments = self.segments[1:]
        return self.segments
    
    
def main():
    """Основная функция"""
    music = Music_row('w.wav')
    music.load_and_preprocess()
    music.extract_pitch_with_crepe()
    print(music.filter_notes())

    """Опционально: создание MIDI-файла"""
    #midi_data = pretty_midi.PrettyMIDI()
    #instrument = pretty_midi.Instrument(program=0)

    #for segment in quantized_segments:
        #if segment["note"] != -1:
            #note = pretty_midi.Note(velocity=100, pitch=int(segment["note"]), start=segment["start_time"], end=segment["end_time"])
            #instrument.notes.append(note)

    #midi_data.instruments.append(instrument)
    #midi_data.write("output.mid")
    #print("MIDI файл output.mid создан.")

if __name__ == "__main__":
    main()