import os
import json
from core.constants import LANGUAGES
from core.paths import CONFIG_PATH, TRANSLATE_PATH
from core.utils import get_yes_no, clear_console

def load_translations(lang):
    """Loads translations for interface."""
    if not os.path.exists(TRANSLATE_PATH):
        return {"enter_language_code": "Enter language code: ",
                "invalid_code": "Invalid code. Try again:",
                "repeat_question": "Repeat questions on startup?",
                "translate_description": "Translate mod descriptions?"}
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
        "repeat_question": repeat,  # This parameter controls settings re-prompt
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
