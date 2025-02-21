import os
import re
import json
from core.func import find_steam_workshop
from core.constants import *

def get_yes_no(question):
    """Requests a yes/no answer."""
    while True:
        answer = input(f"{question} ").strip().lower()
        if answer in ["y", "yes"]:
            return True
        elif answer in ["n", "no"]:
            return False
        print("Invalid input, please enter 'y' or 'n'.")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

from core.config import load_config, load_translations
config = load_config()  # Keep only one initialization
texts = load_translations(config["lang"])  # Keep only one initialization
WORKSHOP_PATH = find_steam_workshop()

# Check for mods presence
mod_list = [mod_id for mod_id in os.listdir(WORKSHOP_PATH) if os.path.isdir(os.path.join(WORKSHOP_PATH, mod_id))]
if not mod_list:
    print(f"{RED}{texts['no_mods']}{RESET}")
    input(texts['press_enter_exit'])
    exit(0)

async def translate_text(text, translator):
    """Translates text to selected language."""
    translated = await translator.translate(text, src="en", dest=config["lang"])
    return translated.text.capitalize()

def get_mod_name(mod_path):
    """Gets mod name from description.json."""
    description_file = os.path.join(mod_path, "description.json")
    if os.path.exists(description_file):
        try:
            with open(description_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get("name", os.path.basename(mod_path))
        except json.JSONDecodeError:
            return os.path.basename(mod_path)
    return os.path.basename(mod_path)

def clean_json(content):
    """Removes comments and fixes errors in JSON file."""
    content = re.sub(r'//.*', '', content)  # Remove single-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)  # Remove multi-line comments
    content = re.sub(r'[\x00-\x1F\x7F]', '', content)  # Remove control characters
    content = re.sub(r',\s*}', '}', content)  # Remove commas before closing curly brace
    content = re.sub(r',\s*]', ']', content)  # Remove commas before closing square bracket
    content = content.replace('\n', ' ')  # Remove line breaks
    return content.strip()
