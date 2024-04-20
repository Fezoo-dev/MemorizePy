import asyncio
import threading
import tkinter as tk
from dictionary import Dictionary

class Window:
    def __init__(self, fileName: str, separator: str = ",", langQuiz: str = "Russian", langAnswer: str = "Russian"):
        self._dictionary = Dictionary(fileName, separator, langQuiz, langAnswer)

    def run(self, timeout: int):

        self._root = tk.Tk(baseName='window')
        self._root.wm_attributes("-topmost", True)
        self._root.bind('<Return>', lambda event: self.__set_result())

        self._answerField = tk.Entry(self._root)
        self._answerField.pack(side=tk.LEFT)
        self._answerField.focus()

        button = tk.Button(self._root, text='Submit', command=lambda: self.__set_result())
        button.pack(side=tk.LEFT)

        asking = threading.Thread(target=asyncio.run, args=(self._dictionary.run(timeout), ))
        asking.start()
        
        self._root.lift()
        tk.mainloop()
        self._dictionary.stop()
        asking.join(timeout)

    def __set_result(self):
        answer = self._answerField.get()
        self._answerField.delete(0, tk.END)
        
        right_answer = self._dictionary.get_answer()
        if answer != right_answer:
            self._answerField.insert(0, right_answer)

        self._answerField.focus()
        threading.Thread(target=asyncio.run, args=(self._dictionary.tell_answer(answer), )).start()
        