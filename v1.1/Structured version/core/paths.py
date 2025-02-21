import os
import sys

# Define path to `config.json`
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)  # Path if program is packaged as .exe
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Regular path for .py

OUTPUT_PATH = os.path.join(BASE_DIR, 'Translate mods')
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
TRANSLATE_PATH = os.path.join(BASE_DIR, "data", "translates.json")
