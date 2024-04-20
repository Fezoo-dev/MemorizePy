import asyncio
import random
import pyttsx3
from os.path import exists

import pyttsx3.voice

class Dictionary:
    def __init__(self, fileName: str, separator: str, langQuiz: str, langAnswer: str) -> None:
        self._engine = pyttsx3.init()

        voices = self._engine.getProperty('voices')
        self._askLang = self.__find_lang_object(langQuiz, voices)
        self._answerLang = self.__find_lang_object(langAnswer, voices)

        if self._askLang is None:
            Exception("Language `" + langQuiz + "` not found")

        if self._answerLang is None:
            Exception("Language `" + langAnswer + "` not found")

        rate = self._engine.getProperty('rate')
        self._engine.setProperty('rate', rate-50)

        text = self.__read_file(fileName)
        self.keys, self._d = self.__parse_file(text, separator)


    def __find_lang_object(self, lang: str, voices: list) -> pyttsx3.voice.Voice:
        return next(l for l in voices if lang in l.name)


    async def run(self, timeout: int):
        self._stopThread = False
        while not self._stopThread:
            self._word = random.choice(self.keys)
            self._engine.setProperty('voice', self._askLang.id)
            self._engine.say(self._word)
            self._engine.runAndWait()
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
        self._engine.runAndWait()

    def __read_file(self, fileName: str) -> str:
        if not exists(fileName):
            err = "The file " + fileName + " doesn't exist"
            return err + "," + err
        with open(fileName, mode="r+") as f:
            return f.read()
            
    def __parse_file(self, text: str, separator: str) -> {list, dict}:
        keys = []
        d = dict()
        for line in text.split('\n'):
            pair = line.split(separator)
            keys.append(pair[0])
            d[pair[0]] = pair[1]

        return keys, d