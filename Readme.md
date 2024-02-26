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
pip install deepl 
Указанная команда установит библиотеку для работы с API DeepL (deepl) 

Получение API ключа для DeepL:
Зарегистрируйтесь на сайте DeepL и получите API ключ. Инструкции по получению ключа доступны в документации DeepL.

Настройка скрипта:
Откройте config.json в текстовом редакторе и замените значение переменных, api_key на ваш личный API ключ от DeepL.

Запуск скрипта:
Откройте командную строку в папке с вашим проектом и выполните команду:
py

Порядок запуска:
1) Сначала в рабочей папке сохраняем нужный нам глоссарий. Пишем в поле "DeepL_glossary_name" В файле config.json желаемое имя глоссарий в DeepL и имя в папке.
2) Регистрируем его в DeepL используя код CreateDeepL_Glossary. Это заполнит поле glossary id.
3) Заполяем путь до желаемого к переводу JSON файла приключения из foundry. Обычно лучше хранить в originals.
4) Запускаем код DeepLAdvTranslate


Поддерживаемые языки/supported languages:
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


Autotranslation module of adventures for Foundry. Translation is done via DeepL.
Version 0.5 beta

What it does:
Translates logs (content, page titles, log titles) scene titles, monster abilites, actor names via DeepL in accordance with the glossary.

Algorithm of work:
-Program reads JSON file, 
-extracts from it in the format of lines for translation, 
-deposits them into the files work/<JSON name>_extracted.json
-first stop step. Do we do the translation?
-Checks if there is a translation of the given strings in the translation buffer. 
-If there is translation in the buffer - translation is taken from there, translates missing ones from DEEPL filling the buffer file with new data.
-Second stop step. Whether we form JSON file of adventure with translation.
-Forming a JSON file of the adventure and

How to use:

Download and install the latest version of Python from the official python.org website.
During installation, be sure to tick the "Add Python to PATH" option to use Python from the command line.

Install the required libraries:
Open a command prompt (CMD or PowerShell) and install the following libraries using the pip package manager:
pip install deepl 
The above command will install the library to work with the API DeepL (deepl) 

Obtain an API key for DeepL:
Register at DeepL and get an API key. Instructions for obtaining the key are available in the documentation at DeepL.

Configuring the script:
Open config.json in a text editor and replace the value of the variables, api_key with your personal API key from DeepL.

Running the script:
Open a command prompt in your project folder and run the command:
py

Launch order:
1) First, save the glossary we need in the working folder. We write in the field "DeepL_glossary_name" in the config.json file the desired name of the glossary in DeepL and the name in the folder.
2) Register it in DeepL using the CreateDeepL_Glossary code. This will populate the glossary id field.
3) Fill in the path to the desired JSON file of the adventure from foundry. Usually it is better to store it in originals.
4) Run the DeepLAdvTranslate code
