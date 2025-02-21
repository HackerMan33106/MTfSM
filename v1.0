import os
import re
import sys
import json
import shutil
import winreg
import asyncio
from aiogoogletrans import Translator

# Determine the path to the `.exe` folder if the program is compiled
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)  # Folder where the .exe is located
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Standard path for .py

# ANSI escape sequences for colors
GREEN = "\033[92m"  # Green
RED = "\033[91m"    # Red
RESET = "\033[0m"   # Reset color
PURPLE = "\033[95m"  # Purple
CYAN = "\033[96m"    # Cyan

def find_steam_workshop():
    """Finds the Steam folder via the registry and returns the path to the Scrap Mechanic workshop."""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam") as key:
            steam_path, _ = winreg.QueryValueEx(key, "InstallPath")  # Get the Steam path
    except FileNotFoundError:
        raise FileNotFoundError("Steam not found in the registry! It may not be installed.")

    # Path to the Scrap Mechanic workshop
    workshop_path = os.path.join(steam_path, "steamapps", "workshop", "content", "387990")
    
    if not os.path.exists(workshop_path):
        raise FileNotFoundError("Scrap Mechanic workshop folder not found!")
    
    return workshop_path

# Source path with mods (searching via registry)
try:
    WORKSHOP_PATH = find_steam_workshop()
except FileNotFoundError as e:
    print(f"{RED}Error: {e}{RESET}")
    input("Press Enter to exit...")
    exit(1)

# Check if there are any mods
mod_list = [mod_id for mod_id in os.listdir(WORKSHOP_PATH) if os.path.isdir(os.path.join(WORKSHOP_PATH, mod_id))]
if not mod_list:
    print(f"{RED}No mods available for translation!{RESET}")
    input("Press Enter to exit...")
    exit(0)

# Path to save translated mods
OUTPUT_PATH = os.path.join(BASE_DIR, 'Translate mods')

# Function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def clean_json(content):
    """Removes comments and fixes errors in the JSON file."""
    # Remove lines starting with //
    content = re.sub(r'//.*', '', content)
    # Replace incorrect line breaks in values
    content = content.replace('\n', ' ')
    return content

async def translate_text(text, translator):
    """Translates text from English to Russian and capitalizes the first letter."""
    translated = await translator.translate(text, src='en', dest='ru')
    return translated.text.capitalize()

async def process_file(file_path, output_file, translator):
    """Opens, cleans, translates, and saves a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cleaned_content = clean_json(content)  # Clean JSON from unwanted characters
        data = json.loads(cleaned_content)  # Load cleaned JSON
        
        # Iterate through all keys in the JSON file and translate title and description
        for key, value in data.items():
            if 'title' in value:
                value['title'] = await translate_text(value['title'], translator)
            if 'description' in value:
                value['description'] = await translate_text(value['description'], translator)
        
        # Save the translated data back to the file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"{GREEN}Translated file: {output_file}{RESET}")
    except json.JSONDecodeError as e:
        print(f"{RED}JSON processing error in {file_path}: {e}{RESET}")
    except Exception as e:
        print(f"{RED}Error processing {file_path}: {e}{RESET}")

async def process_mod(mod_id, translator):
    """Processes a mod: creates folder structure and translates files."""
    mod_path = os.path.join(WORKSHOP_PATH, mod_id)
    target_path = os.path.join(OUTPUT_PATH, mod_id, "Gui", "Language")
    
    # Path to the original English folder, from where files are taken for translation
    gui_path = os.path.join(mod_path, "Gui", "Language", "English")
    if not os.path.exists(gui_path):
        return  # If the folder does not exist, skip the mod
    
    # Create a Russian translation folder if it does not exist
    russian_path = os.path.join(target_path, "Russian")
    os.makedirs(russian_path, exist_ok=True)
    
    # Iterate through files in the English folder, copy only JSON files and translate them
    for file in os.listdir(gui_path):
        if file.endswith('.json'):  # Check if the file is JSON
            source_file = os.path.join(gui_path, file)
            target_file = os.path.join(russian_path, file)
            
            shutil.copy(source_file, target_file)  # Copy the file
            await process_file(target_file, target_file, translator)  # Translate the file

async def main():
    """Main function: finds mods and starts processing them."""
    clear_console()
    print(f"{CYAN}Scrap Mechanic Mod Translator v1.0{RESET}")
    os.makedirs(OUTPUT_PATH, exist_ok=True)  # Create output folder if it does not exist
    translator = Translator()  # Create a translator object
    
    tasks = []
    for mod_id in os.listdir(WORKSHOP_PATH):
        mod_path = os.path.join(WORKSHOP_PATH, mod_id)
        if os.path.isdir(mod_path):  # Check if it is a folder
            tasks.append(process_mod(mod_id, translator))
    
    await asyncio.gather(*tasks)  # Start asynchronous processing of all mods
    print(f"{PURPLE}Translation complete!{RESET}")

    input("Press Enter to exit...")  # Wait for Enter key press

if __name__ == "__main__":
    asyncio.run(main())  # Run the main function
