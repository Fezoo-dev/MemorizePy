import asyncio
import csv
import random
import pyttsx3
import pyttsx3.voice
from os.path import exists
from settings import Settings


class Dictionary:
    def __init__(self, settings: Settings) -> None:
        self._engine = pyttsx3.init()

        voices = self._engine.getProperty('voices')
        self._askLang = self.__find_lang_object(settings.langQuiz, voices)
        self._answerLang = self.__find_lang_object(settings.langAnswer, voices)

        if self._askLang is None:
            Exception("Language `" + settings.langQuiz + "` not found")

        if self._answerLang is None:
            Exception("Language `" + settings.langAnswer + "` not found")

        rate = self._engine.getProperty('rate')
        self._engine.setProperty('rate', rate-50)

        self.keys, self._d = self.__read_csv_like_file(settings)

    def __find_lang_object(self, lang: str, voices: list) -> pyttsx3.voice.Voice:
        return next(l for l in voices if lang in l.name)


    async def run(self, timeout: int):
        self._stopThread = False
        while not self._stopThread:
            self._word = random.choice(self.keys)
            self._engine.setProperty('voice', self._askLang.id)
            self._engine.say(self._word)
            try:
                self._engine.runAndWait()
            except:
                pass
            dt = 0
            while dt < timeout and not self._stopThread:
                dt += 1
                await asyncio.sleep(1)

    def stop(self):
        self._engine.stop()
        self._stopThread = True
    
    def get_answer(self) -> str:
        return self._d[self._word]

    async def tell_answer(self, answer: str) -> None:
        right_answer = self._d[self._word]
        correct = answer == right_answer

        self._engine.setProperty('voice', self._answerLang.id)
        phrase = "Correct. The answer is " if correct else "Wrong. The correct answer is "
        self._engine.say(phrase)
        self._engine.say(right_answer)
        try:
            self._engine.runAndWait()
        except:
            pass

    def __read_csv_like_file(self, settings: Settings) -> {list, dict}:
        if not exists(settings.fileName):
            err = "The file " + settings.fileName + " doesn't exist"
            return err + "," + err
        with open(settings.fileName, mode="r+") as f:
            reader = csv.reader(f, delimiter=settings.delimeter)
            for _ in range(0, settings.headerLines):
                next(reader)
            keys = []
            d = dict()
            for row in reader:
                keys.append(row[settings.questionIndex])
                d[row[settings.questionIndex]] = row[settings.answerIndex]

            return keys, d
