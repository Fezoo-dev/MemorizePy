import json
import tkinter as tk
from pathlib import Path
from settings import Settings
from window import Window

class Memorizer:
    def __init__ (self, basedir: Path):
        self._csv_folder = basedir / "csv"
        self._json_folder = basedir / "json"
        self.__create_folders(self._csv_folder, self._json_folder)
        self._default_json = self.__create_default_json(self._json_folder / "default.json")
        self.__fill_jsons()

        self.__show_settings_window()

    def __create_folders(self, *paths: Path):
        for path in paths:
            if not path.exists():
                path.mkdir()

    def __create_default_json(self, defaultPath: Path):
        if not defaultPath.exists():
            with open(defaultPath, "w") as f:
                f.write(self.__get_default_json())
        with open(defaultPath, "r") as f:
            return f.read()

    def __fill_jsons(self):
        self._csvs = [path.name[0:-4] for path in self._csv_folder.glob("*.csv")]
        jsons = [path.name[0:-5] for path in self._json_folder.glob("*.json")]

        for csv in self._csvs:
            if csv not in jsons:
                with open(self._json_folder / (csv + ".json"), "w") as f:
                    f.write(self._default_json)

    def __get_default_json(self):
        return json.dumps({
            "delimeter": ",",
            "langQuiz": "English",
            "langAnswer": "English",
            "questionIndex": 0,
            "answerIndex": 1,
            "headerLines": 0,
            "timeout": 30
        })
    
    def __show_settings_window(self):
        self._root = tk.Tk(baseName='window')
        self._root.wm_attributes("-topmost", True)
        self._root.bind('<Return>', lambda event: self.__set_result())

        self._file = tk.StringVar(self._root)
        self._file.set(self._csvs[0])
        dropdown = tk.OptionMenu(self._root, self._file, *self._csvs)
        dropdown.pack(side=tk.LEFT)

        button = tk.Button(self._root, text='Start', command=lambda: self.__open_main_window())
        button.pack(side=tk.LEFT)

        self._root.lift()
        tk.mainloop()

    def __open_main_window(self):
        self._root.destroy()
        settings = self.__read_json_settings()
        window = Window(settings=settings)
        window.run(settings.timeout)
        
    def __read_json_settings(self) -> Settings:
        s = self._json_folder / (self._file.get() + ".json")
        with open(s, "r") as f:
            json_settings = json.load(f)
        
        settings = self.__convert_json_to_settingsdef(json_settings)
        settings.fileName = self._csv_folder / (self._file.get() + ".csv")
        return settings
    
    def __convert_json_to_settingsdef (self, *initial_data, **kwargs) -> Settings:
        settings = Settings()
        for dictionary in initial_data:
            for key in dictionary:
                setattr(settings, key, dictionary[key])
        for key in kwargs:
            setattr(settings, key, kwargs[key])

        return settings