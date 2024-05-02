import csv
import json
import tkinter as tk
from tkinter import filedialog as fd
from pathlib import Path
from settings import Settings
from window import Window

class Memorizer:
    def __init__ (self, basedir: Path):
        self._json_folder = basedir / "json"
        self.__create_folders(self._json_folder)

        self.__show_settings_window()

    def __create_folders(self, *paths: Path) -> None:
        for path in paths:
            if not path.exists():
                path.mkdir()

    def __get_settings(self) -> list[str]:
        return [f.name[0:-5] for f in self._json_folder.glob('*.json')]

    def __get_default_json(self, filename: str) -> str:

        return json.dumps({
            "pathToFile": filename,
            "delimiter": self.__get_delimiter(filename),
            "langQuiz": "English",
            "langAnswer": "English",
            "questionIndex": 0,
            "answerIndex": 1,
            "headerLines": 0,
            "timeout": 30
        })
    
    def __show_settings_window(self) -> None:
        self._root = tk.Tk(baseName='window')
        self._root.wm_attributes("-topmost", True)

        add_button = tk.Button(self._root, text='Add database', command=lambda: self.__add_json(), bg='green')
        add_button.pack(side=tk.TOP, fill=tk.X)
        
        self._file = tk.StringVar(self._root)
        self._dropdown = tk.OptionMenu(self._root, self._file, [])
        self._dropdown.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self._start_training_button = tk.Button(self._root, text='Start training', command=lambda: self.__open_main_window(), bg='yellow')
        self._start_training_button.pack(side=tk.LEFT)
        
        self._delete_button = tk.Button(self._root, text='Delete selected', command=lambda: self.__delete_json(), bg='red')
        self._delete_button.pack(side=tk.LEFT, fill=tk.X)

        self.__update_ui()
        self.__select_default()

        self._root.lift()
        tk.mainloop()

    def __update_ui(self) -> None:
        self.__update_dropdown()
        state = 'normal' if len(self._jsons) > 0 else 'disabled'
        self._start_training_button['state'] = state
        self._delete_button['state'] = state

    def __update_dropdown(self) -> None:
        self._jsons = self.__get_settings()
        self._dropdown['menu'].delete(0, 'end')
        for json in self._jsons:
            self._dropdown['menu'].add_command(label=json, command=tk._setit(self._file, json))

    def __select_default(self) -> None:
        if len(self._jsons) == 0:
            self._file.set("")
        else:
            self._file.set(self._jsons[0])


    def __delete_json(self) -> None:
        selected = self._file.get()
        (self._json_folder / (selected + ".json")).unlink()
        self._jsons.remove(selected)
        self.__update_ui()
        self.__select_default()

    def __add_json(self) -> None:
        filetypes = (('csv files', '*.csv'),('All files', '*.*'))

        filename = fd.askopenfilename(
            title='Choose your database file.',
            initialdir='~/',
            filetypes=filetypes)

        if not filename:
            return
        
        key = Path(filename).stem
        json_file_name = self._json_folder / (key + ".json")

        with open(json_file_name, "w") as f:
            f.write(self.__get_default_json(filename))

        self._jsons.append(key)
        self.__update_ui()
        self._file.set(key)

    def __get_delimiter(self, filename):
        sniffer = csv.Sniffer()
        with open(filename) as fp:
            delimiter = sniffer.sniff(fp.read(500)).delimiter
        return delimiter

    def __open_main_window(self):
        self._root.destroy()
        settings = self.__read_json_settings()
        window = Window(settings=settings)
        window.run(settings.timeout)
        
    def __read_json_settings(self) -> Settings:
        s = self._json_folder / (self._file.get() + ".json")
        with open(s, "r") as f:
            json_settings = json.load(f)
        
        settings = self.__convert_json_to_settings(json_settings)
        return settings
    
    def __convert_json_to_settings (self, *initial_data, **kwargs) -> Settings:
        settings = Settings()
        for dictionary in initial_data:
            for key in dictionary:
                setattr(settings, key, dictionary[key])
        for key in kwargs:
            setattr(settings, key, kwargs[key])

        return settings