Модуль автоперевода приключений для Foundry. Перевод выполняется через сервис DeepL.
Version 0.5 beta

Что делает:
Переводит журналы (содержимое, название страниц, название журналов) название сцен, абилки монстры, имена актеров через DeepL в соотвествии с глоссарием.

Алгоритм работы:
-Программа читает JSON файл, 
-извлекает из него в формате строчки для перевода, 
-откладывает из в файлы work/<имя JSON>_extracted.json
-первый шаг остановки. Делаем ли перевод?
-После чего проверяет есть ли перевод данных строк в буфере перевода. 
-Если в буфере перевод есть - перевод берется оттуда, переводит недостающие из DEEPL заполняя файла буфера новыми данными
-Второй шаг остановки. Формируем ли JSON файл приключения с переводом.
-формирование JSON файла приключения и

Как использовать:

Скачайте и установите последнюю версию Python с официального сайта python.org.
Во время установки обязательно отметьте опцию "Add Python to PATH", чтобы использовать Python из командной строки.
Установка необходимых библиотек:

Откройте командную строку (CMD или PowerShell) и установите следующие библиотеки с помощью пакетного менеджера pip:
Copy code
pip install deepl hashlib
Указанная команда установит библиотеку для работы с API DeepL (deepl) и встроенную библиотеку для работы с хешированием (hashlib уже включена в стандартную библиотеку Python, поэтому её устанавливать не нужно).
Получение API ключа для DeepL:

Зарегистрируйтесь на сайте DeepL и получите API ключ. Инструкции по получению ключа доступны в документации DeepL.

Подготовка рабочей среды:

Создайте на компьютере папку, куда будете сохранять свой скрипт и необходимые файлы (например, MyProject).
Сохраните ваш скрипт в эту папку.
Создайте внутри папки MyProject дополнительные папки work, result, и originals, как указано в скрипте.
Настройка скрипта:

Откройте config.json в текстовом редакторе и замените значение переменной api_key на ваш личный API ключ от DeepL.
Убедитесь, что пути к файлам в скрипте соответствуют вашей структуре папок.

Запуск скрипта:

Откройте командную строку в папке с вашим проектом и выполните команду:
Copy code
python имя_вашего_скрипта.py
Следуйте инструкциям в скрипте для выполнения перевода.

Порядок запуска:
1) Сначала в рабочей папке сохраняем нужный нам глоссарий. Пишем в поле "DeepL_glossary_name" В файле config.json желаемое имя глоссарий в DeepL
2) Регистрируем его в DeepL используя код CreateDeepL_Glossary. Это заполнит поле glossary id.
3) Заполяем путь до желаемого к переводу JSON файла приключения из foundry. Обычно лучше хранить в originals.
4) Запускаем код DeepLAdvTranslate


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
DE (German)
EN (English)
ES (Spanish)
FR (French)
IT (Italian)
JA (Japanese)
NL (Dutch)
PL (Polish)
PT (Portuguese)
RU (Russian)
ZH (Chinese)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Autotranslation module of adventures for Foundry. Translation is done via DeepL. Version 0.5 beta

What does it do: Translates logs (content, page names, log names) scene names, monster abils, actor names via DeepL in accordance with the glossary.

Algorithm of work: -Program reads JSON file, -extracts from it in the format of lines for translation, -posts from it to the files work/<name JSON>_extracted.json -first stop step. Do we do the translation? -Checks if there is a translation of the given strings in the translation buffer. -If there is a translation in the buffer, the translation is taken from there, translates the missing ones from DEEPL filling the buffer file with new data -Second stop step. Whether we form JSON file of adventure with translation. -Forming a JSON file of the adventure and

How to use:

Download and install the latest version of Python from the official python.org website. During installation, be sure to tick the "Add Python to PATH" option to use Python from the command line. Install the required libraries:

Open a command line (CMD or PowerShell) and install the following libraries using the pip package manager: Copy code pip install deepl hashlib The above command will install the DeepL API key library (deepl) and the built-in hashing library (hashlib is already included in the Python standard library, so you don't need to install it). Obtain an API key for DeepL:

Register at DeepL to get an API key. Instructions for obtaining the key are available in the documentation at DeepL.

Preparing a working environment:

Create a folder on your computer where you will save your script and necessary files (e.g. MyProject). Save your script to this folder. Create additional work, result, and originals folders inside the MyProject folder as specified in the script. Configuring the script:

Open config.json in a text editor and replace the value of the api_key variable with your personal API key from DeepL. Make sure the file paths in the script match your folder structure.

Running the script:

Open a command prompt in your project folder and run the command: Copy code python name_your_script.py Follow the instructions in the script to perform the translation.

Startup order:

First, in the working folder, save the glossary we need. We write in the field "DeepL_glossary_name" in the config.json file the desired name of the glossary in DeepL.
Register it in DeepL using the code CreateDeepL_Glossary. This will populate the glossary id field.
Fill in the path to the desired JSON file to translate the adventure from foundry. Usually it is better to store it in originals.
Run the DeepLAdvTranslate code
