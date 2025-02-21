import os
import json
import shutil
from core.utils import WORKSHOP_PATH, translate_text, clean_json, get_mod_name, config, texts
from core.constants import LANGUAGE_FOLDERS, GREEN, RED, RESET
from core.paths import OUTPUT_PATH

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
    """Copies and translates description.json only if enabled in settings."""
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
