import os
from pathlib import Path
from settings_window import Memorizer

program_dir = Path(os.path.dirname(__file__)).parent
Memorizer(program_dir)