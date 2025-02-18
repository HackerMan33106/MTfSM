import os
import re
import sys
import json
import shutil
import winreg
import asyncio
from aiogoogletrans import Translator

# Определяем путь к папке с `.exe`, если программа скомпилирована
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)  # Папка, где находится .exe
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Обычный путь для .py

# ANSI escape sequences для цветов
GREEN = "\033[92m"  # Зеленый
RED = "\033[91m"    # Красный
RESET = "\033[0m"   # Сброс цвета
PURPLE = "\033[95m"  # Фиолетовый
CYAN = "\033[96m" # Голубой

def find_steam_workshop():
    """Ищет папку Steam через реестр и возвращает путь к мастерской Scrap Mechanic."""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam") as key:
            steam_path, _ = winreg.QueryValueEx(key, "InstallPath")  # Получаем путь к Steam
    except FileNotFoundError:
        raise FileNotFoundError("Steam не найден в реестре! Возможно, он не установлен.")

    # Путь к мастерской Scrap Mechanic
    workshop_path = os.path.join(steam_path, "steamapps", "workshop", "content", "387990")
    
    if not os.path.exists(workshop_path):
        raise FileNotFoundError("Папка мастерской Scrap Mechanic не найдена!")
    
    return workshop_path

# Исходный путь с модами (ищем через реестр)
try:
    WORKSHOP_PATH = find_steam_workshop()
except FileNotFoundError as e:
    print(f"{RED}Ошибка: {e}{RESET}")
    input("Нажмите Enter для выхода...")
    exit(1)

# Проверка на наличие модов
mod_list = [mod_id for mod_id in os.listdir(WORKSHOP_PATH) if os.path.isdir(os.path.join(WORKSHOP_PATH, mod_id))]
if not mod_list:
    print(f"{RED}Нет модов для перевода!{RESET}")
    input("Нажмите Enter для выхода...")
    exit(0)

# Путь сохранения перевода
OUTPUT_PATH = os.path.join(BASE_DIR, 'Translate mods')

# Функция для очистки консоли
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def clean_json(content):
    """Удаляет комментарии и исправляет ошибки в JSON-файле."""
    # Удаляем строки, начинающиеся с //
    content = re.sub(r'//.*', '', content)
    # Заменяем некорректные переводы строк в значениях
    content = content.replace('\n', ' ')
    return content

async def translate_text(text, translator):
    """Переводит текст с английского на русский и делает первую букву заглавной."""
    translated = await translator.translate(text, src='en', dest='ru')
    return translated.text.capitalize()

async def process_file(file_path, output_file, translator):
    """Открывает, очищает, переводит и сохраняет JSON-файл."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cleaned_content = clean_json(content)  # Чистим JSON от мусора
        data = json.loads(cleaned_content)  # Загружаем очищенный JSON
        
        # Перебираем все ключи в JSON-файле и переводим title и description
        for key, value in data.items():
            if 'title' in value:
                value['title'] = await translate_text(value['title'], translator)
            if 'description' in value:
                value['description'] = await translate_text(value['description'], translator)
        
        # Записываем переведённые данные обратно в файл
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"{GREEN}Переведён файл: {output_file}{RESET}")
    except json.JSONDecodeError as e:
        print(f"{RED}Ошибка обработки JSON в {file_path}: {e}{RESET}")
    except Exception as e:
        print(f"{RED}Ошибка при обработке {file_path}: {e}{RESET}")

async def process_mod(mod_id, translator):
    """Обрабатывает мод: создаёт структуру папок и переводит файлы."""
    mod_path = os.path.join(WORKSHOP_PATH, mod_id)
    target_path = os.path.join(OUTPUT_PATH, mod_id, "Gui", "Language")
    
    # Путь к оригинальной папке English, откуда берутся файлы для перевода
    gui_path = os.path.join(mod_path, "Gui", "Language", "English")
    if not os.path.exists(gui_path):
        return  # Если папки нет, пропускаем мод
    
    # Создаём папку Russian для перевода, если её нет
    russian_path = os.path.join(target_path, "Russian")
    os.makedirs(russian_path, exist_ok=True)
    
    # Перебираем файлы в папке English, копируем только JSON-файлы и переводим их
    for file in os.listdir(gui_path):
        if file.endswith('.json'):  # Проверяем, является ли файл JSON
            source_file = os.path.join(gui_path, file)
            target_file = os.path.join(russian_path, file)
            
            shutil.copy(source_file, target_file)  # Копируем файл
            await process_file(target_file, target_file, translator)  # Переводим файл

async def main():
    """Основная функция: находит моды и запускает их обработку."""
    clear_console()
    print(f"{CYAN}Переводчик модов Scrap Mechanic v1.0{RESET}")
    os.makedirs(OUTPUT_PATH, exist_ok=True)  # Создаём выходную папку, если её нет
    translator = Translator()  # Создаём объект переводчика
    
    tasks = []
    for mod_id in os.listdir(WORKSHOP_PATH):
        mod_path = os.path.join(WORKSHOP_PATH, mod_id)
        if os.path.isdir(mod_path):  # Проверяем, что это папка
            tasks.append(process_mod(mod_id, translator))
    
    await asyncio.gather(*tasks)  # Запускаем асинхронную обработку всех модов
    print(f"{PURPLE}Перевод завершён!{RESET}")

    input("Нажмите Enter для выхода...")  # Ждём нажатия Enter

if __name__ == "__main__":
    asyncio.run(main())  # Запускаем основную функцию
