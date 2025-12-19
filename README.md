# <ins>English Version</ins>:
# MTfSM – Scrap Mechanic Mod Translator to 11 Languages
💡 **This tool allows you to translate Scrap Mechanic mods into 11 languages.** Now you can translate mods not only from English to Russian but also into other languages using AI. The program supports most mods, but there may be small inaccuracies since machine translation is used.

📌 **The program supports 11 languages:** Russian, English, Chinese, Spanish, German, French, Portuguese, Italian, Japanese, Korean, and Polish.

⏳ **If the program "freezes"**, just wait – it might be processing a large mod, which can take some time.

## 🔧 How the Program Works
When you launch the program (main.exe), it automatically:

1. Finds the Steam installation and the Scrap Mechanic mods folder (steamapps\workshop\content\387990).
2. Checks for the presence of mods – if none are found, it shows a message and exits.
3. Creates a Translate mods folder in the same directory where the program is located.
4. Copies the original files from the mod's English folder into a new folder (e.g., Russian or another language, depending on the settings).
5. Translates JSON files (only the title and description fields) from the source language to the selected one.
6. Saves the translated files in the Translate mods folder without changing the original files.

**⚠️ The program processes only JSON files from the Gui/Language/English folder. If the mod doesn't contain such files, it will be skipped.**

## 📖 Instructions for Use
1. Run main.exe – the translation process will begin automatically.
2. During the process, the program will ask several questions:
- Choose the translation language (you can select from 11 available languages).
- Whether to translate the description.
- Specify the path to the mods folder if it’s not automatically found.
3. Wait for the translation to complete – once done, the program will ask you to press any key to exit.
4. Open the Translate mods folder – translated versions of the mods will be there.
5. Replace the files in the mod folder if necessary – by default, the program does not modify the original files.
  
**If the program can't find the mods, make sure there are files in the folder.**

## 🔹 Compiling and Modifying the Code
**MTfSM is an open-source project, and you can modify it to suit your needs.**

💾 To build the .exe from main.py:

1. Open the program folder.
2. Place the modified main.py in the same folder as the compiler.
3. Run the compiler as administrator.
4. After compiling, the .exe file will be moved to the compiler folder, and temporary files will be deleted.
### 🔹 Additional Features and Plans
💡 If there are no bugs then this will be the last MTfSM update!

✅ Fully autonomous process – no setup required.

✅ Automatic Steam path detection – the program works on any system with Steam installed.

✅ Support for 11 languages – translation is now available in 11 languages, including Russian, English, Chinese, Spanish, German, and others.

⚙️ Handling large mods – optimization has been added to improve the program’s ability to handle large mods without freezing. The program now processes mods faster and with less system load.

🚀 Updates and fixes – we are continuously improving the code and fixing bugs for more stable operation.

# <ins>Русская версия</ins>:

# MTfSM – Переводчик модов Scrap Mechanic на 11 языков
💡 **Данный инструмент позволяет переводить моды для Scrap Mechanic на 11 языков.** Теперь вы можете переводить моды не только с английского на русский, но и на другие языки с помощью ИИ. Программа поддерживает большинство модов, однако могут встречаться небольшие неточности, так как используется машинный перевод.

📌 **Программа поддерживает 11 языков:** русский, английский, китайский, испанский, немецкий, французский, португальский, итальянский, японский, корейский, и польский.

⏳ **Если программа "зависла"**, просто подождите – возможно, она обрабатывает большой мод, что может занять некоторое время.

## 🔧 Как работает программа
При запуске программы (main.exe) она автоматически:

1. Находит установку Steam и папку с модами Scrap Mechanic (steamapps\workshop\content\387990).
2. Проверяет наличие модов – если их нет, выводит сообщение и завершает работу.
3. Создаёт папку Translate mods в той же директории, где запущена программа.
4. Копирует оригинальные файлы из папки English мода в новую папку Russian (или на другой язык, в зависимости от настроек).
5. Переводит файлы JSON (только поля title и description) с исходного языка на выбранный вами.
6. Сохраняет переведённые файлы в папке Translate mods, не изменяя оригинальные файлы.

**⚠️ Программа обрабатывает только JSON-файлы из папки Gui/Language/English. Если мод не содержит таких файлов, он будет пропущен.**

## 📖 Инструкция по использованию
1. Запустите main.exe – процесс перевода начнётся автоматически.
2. В процессе работы программа задаст несколько вопросов:
- Выбор языка перевода (вы можете выбрать один из 11 доступных языков).
- Переводить ли описание.
- Указание пути к папке с модами, если она не найдена автоматически.
3. Дождитесь завершения перевода – по окончании программа попросит нажать любую клавишу для выхода.
4. Откройте папку Translate mods – там будут находиться переведённые версии модов.
5. Замените файлы в папке мода, если необходимо – по умолчанию программа не изменяет оригинальные файлы.
  
**Если программа не находит моды, убедитесь, что в папке с ними вообще есть файлы.**

## 🔹 Компиляция и изменение кода
**MTfSM – это open-source проект, и вы можете изменять его под свои нужды.**

💾 Для сборки .exe из main.py:

1. Откройте папку с программой.
2. Поместите изменённый main.py в ту же папку, где находится компилятор.
3. Запустите компилятор от имени администратора.
4. После компиляции .exe файл будет перемещён в папку с компилятором, а временные файлы будут удалены.
### 🔹 Дополнительные возможности и планы

💡 Если багов не будет тогда это будет последним обновление MTfSM!

✅ Полностью автономный процесс – не требует настройки.

✅ Автоматическое определение пути Steam – программа работает на любых системах с установленным Steam.

✅ Поддержка 11 языков – теперь доступен перевод на 11 языков, включая русский, английский, китайский, испанский, немецкий и другие.

⚙️ Обработка больших модов – добавлена оптимизация работы программы для обработки крупных модов без зависаний. Программа теперь обрабатывает моды быстрее и с меньшими нагрузками на систему.

🚀 Обновления и исправления – постоянно улучшаем код и исправляем баги для более стабильной работы.
