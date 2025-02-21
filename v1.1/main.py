import os
import sys
import winreg
import json
import shutil
import re
import asyncio
from aiogoogletrans import Translator

# Define path to `config.json`
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)  # Path if program is packaged as .exe
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Regular path for .py

# ANSI escape sequences for colors
GREEN = "\033[92m"  # Green
RED = "\033[91m"    # Red
RESET = "\033[0m"   # Reset color
PURPLE = "\033[95m" # Purple
CYAN = "\033[96m"   # Cyan

# Dictionary of interface languages
LANGUAGES = {
    "br": "Português (Brasil)",
    "zh": "中文",
    "en": "English",
    "fr": "Français",
    "de": "Deutsch",
    "it": "Italiano",
    "ja": "日本語",
    "ko": "한국어",
    "pl": "Polski",
    "ru": "Русский",
    "es": "Español"
}

# Dictionary of localization folder names
LANGUAGE_FOLDERS = {
    "br": "Brazilian",
    "zh": "Chinese",
    "en": "English",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "pl": "Polish",
    "ru": "Russian",
    "es": "Spanish"
}

OUTPUT_PATH = os.path.join(BASE_DIR, 'Translate mods')
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
TRANSLATE_PATH = os.path.join(BASE_DIR, "translates.json")

def find_steam_workshop():
    """Finds Steam folder through registry and returns path to Scrap Mechanic workshop."""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\WOW6432Node\\Valve\\Steam") as key:
            steam_path, _ = winreg.QueryValueEx(key, "InstallPath")
    except FileNotFoundError:
        steam_path = input("Steam not found in registry! Enter Steam path manually: ")
        if not os.path.exists(steam_path):
            print(f"{RED}Error: specified path does not exist!{RESET}")
            exit(1)
    
    workshop_path = os.path.join(steam_path, "steamapps", "workshop", "content", "387990")
    
    if not os.path.exists(workshop_path):
        workshop_path = input("Workshop path not found! Enter path manually: ")
        if not os.path.exists(workshop_path):
            print(f"{RED}Error: specified path does not exist!{RESET}")
            exit(1)
    
    return workshop_path

def load_translations(lang):
    """Loads translations for interface."""
    if not os.path.exists(TRANSLATE_PATH):
        return {"enter_language_code": "Enter language code: ",
                "invalid_code": "Invalid code. Try again: ",
                "repeat_question": "Repeat questions on startup?: ",
                "translate_description": "Translate mod descriptions?: "}
    with open(TRANSLATE_PATH, "r", encoding="utf-8") as f:
        translations = json.load(f)
    return translations.get(lang, translations["en"])

def setup_config():
    """Sets up configuration on first launch or if repeat_question = True."""
    clear_console()
    print("Select language (this affects program language and mod translations):")
    for code, name in LANGUAGES.items():
        print(f"[{code}] {name}")

    while True:
        lang = input("Enter language code: ").strip().lower()
        if lang in LANGUAGES:
            break
        print("Invalid code. Try again:")

    texts = load_translations(lang)
    repeat = get_yes_no(texts["repeat_question"])
    description = get_yes_no(texts["translate_description"])

    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    config = {
        "lang": lang,
        "repeat_question": repeat,  # This parameter controls re-requesting settings
        "translate_description": description
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

    return config

def load_config():
    """Loads configuration or creates new if file doesn't exist."""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)

            # If repeat_question = True, request settings again
            if config.get("repeat_question", False):
                return setup_config()

            return config

    return setup_config()

async def process_file(file_path, output_file, translator, mod_name):
    """Opens, cleans, translates and saves JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cleaned_content = clean_json(content)
        data = json.loads(cleaned_content)
        
        # Fix JSON structure processing
        translated_data = {}
        for key, value in data.items():
            if isinstance(value, dict):
                translated_value = value.copy()
                if 'title' in translated_value:
                    translated_value['title'] = await translate_text(translated_value['title'], translator)
                if 'description' in translated_value:
                    translated_value['description'] = await translate_text(translated_value['description'], translator)
                translated_data[key] = translated_value
            else:
                # If value is string, translate it directly
                translated_data[key] = await translate_text(str(value), translator)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(translated_data, f, ensure_ascii=False, indent=4)
        
        # Form relative path, replacing root folder with mod name
        rel_path = os.path.relpath(output_file, OUTPUT_PATH)
        parts = rel_path.split(os.sep)
        if parts:
            parts[0] = f"[{mod_name}]"
        rel_path = os.sep.join(parts)
        
        print(f"{GREEN}{texts['translated_file']} {rel_path}{RESET}")
    except json.JSONDecodeError as e:
        print(f"{RED}{texts['json_error']} {file_path}: {e}{RESET}")
    except Exception as e:
        print(f"{RED}{texts['processing_error']} {file_path}: {e}{RESET}")

async def process_description(mod_path, translator):
    """Copies and translates description.json only if corresponding setting is enabled."""
    if not config["translate_description"]:  # Check setting
        return
        
    description_file = os.path.join(mod_path, "description.json")
    if not os.path.exists(description_file):
        return
    
    output_file_translate = os.path.join(OUTPUT_PATH, os.path.basename(mod_path), "description.json")
    
    try:
        with open(description_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'description' in data:
            data['description'] = await translate_text(data['description'], translator)
        
        os.makedirs(os.path.dirname(output_file_translate), exist_ok=True)
        with open(output_file_translate, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        mod_name = get_mod_name(mod_path)
        # Display message with mod name
        print(f"{GREEN}{texts['translated_file']} [{mod_name}]{os.sep}description.json{RESET}")
    except json.JSONDecodeError as e:
        print(f"{RED}{texts['json_error']} {description_file}: {e}{RESET}")
    except Exception as e:
        print(f"{RED}{texts['processing_error']} {description_file}: {e}{RESET}")

async def process_mod(mod_id, translator):
    """Processes mod: creates folder structure and translates files."""
    mod_path = os.path.join(WORKSHOP_PATH, mod_id)
    target_path = os.path.join(OUTPUT_PATH, mod_id, "Gui", "Language")
    gui_path = os.path.join(mod_path, "Gui", "Language", "English")
    if not os.path.exists(gui_path):
        return  
    
    mod_name = get_mod_name(mod_path)  # Get mod name
    # Use LANGUAGE_FOLDERS instead of LANGUAGES for correct folder names
    lang_path = os.path.join(target_path, LANGUAGE_FOLDERS[config["lang"]])
    os.makedirs(lang_path, exist_ok=True)
    
    for file in os.listdir(gui_path):
        if file.endswith('.json'):
            source_file = os.path.join(gui_path, file)
            target_file = os.path.join(lang_path, file)
            shutil.copy(source_file, target_file)
            await process_file(target_file, target_file, translator, mod_name)  # Added argument mod_name
    
    await process_description(mod_path, translator)

def get_yes_no(question):
    """Requests yes/no answer."""
    while True:
        answer = input(f"{question} ").strip().lower()
        if answer in ["y", "yes"]:
            return True
        elif answer in ["n", "no"]:
            return False
        print("Invalid input, please enter 'y' or 'n'.")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

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

async def main():
    clear_console()
    print(f"{CYAN}{texts['watermark']}{RESET}")
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    translator = Translator()
    tasks = [process_mod(mod_id, translator) for mod_id in os.listdir(WORKSHOP_PATH) if os.path.isdir(os.path.join(WORKSHOP_PATH, mod_id))]
    await asyncio.gather(*tasks)
    print(f"{PURPLE}{texts['translate_complete']}{RESET}")
    input(texts['press_enter_exit'])
    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
    exit(0)
