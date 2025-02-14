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