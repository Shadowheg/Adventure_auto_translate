# Модуль автоперевода приключений для Foundry
Этот модуль обеспечивает автоперевод контента приключений для Foundry VTT через API DeepL. Версия 0.6 beta.

## Особенности
- Переводит журналы (контент, заголовки страниц, названия журналов), названия сцен, способности монстров и имена актёров.
- Использует DeepL для точных переводов в соответствии с глоссарием.

## Процесс работы
1. Читает JSON файл.
2. Извлекает строки для перевода.
3. Сохраняет их в `work/<имя JSON>_extracted.json`.
4. **Первая контрольная точка:** решение о начале перевода.
5. Проверяет наличие перевода строк в буфере перевода.
6. Если перевод есть в буфере, использует его; в противном случае переводит недостающие строки через DeepL и обновляет файл буфера новыми данными.
7. **Вторая контрольная точка:** решение о формировании JSON файла приключения с переводом.
8. Формирование JSON файла приключения.

## Как использовать

### Скачайте архив DeepLAdvTranslate.rar
ИРаспакуйте в любое удобное место
https://github.com/Shadowheg/Adventure_auto_translate/releases

### Получение API ключа для DeepL
1. Зарегистрируйтесь на сайте DeepL и получите API ключ.
2. В файле config.json замените значение api_key на ваш личный ключ API от DeepL.

### Настройка и запуск скрипта
1. В рабочей папке сохраните нужный глоссарий. В `config.json` укажите имя глоссария в `DeepL_glossary_name`.
2. Зарегистрируйте глоссарий в DeepL с помощью `CreateDeepL_Glossary.bat`. +Это заполнит поле `glossary_id`.
3. Укажите путь к JSON файлу приключения, который вы хотите перевести, обычно лучше хранить его в папке `originals`.
ВНИМАНИЕ:необходимо указывать JSON файл для FOUNDRY типа adventure. Там требуется именно эта разметка.
4. Запустите скрипт `DeepLAdvTranslate.bat`.


## Поддерживаемые языки/supported language
- DE (Немецкий/ German)
- EN (Английский/English)
- ES (Испанский/Spanish)
- FR (Французский/French)
- IT (Итальянский/Italian)
- JA (Японский/Japanese)
- NL (Голландский/Dutch)
- PL (Польский/Polish)
- PT (Португальский/Portuguese)
- RU (Русский/Russian)
- ZH (Китайский/Chinese)

# Adventure Autotranslation Module for Foundry
This module provides auto-translation of adventure content for Foundry VTT via the DeepL API. Version 0.5 beta.

## Features
- Translates logs (content, page titles, log names), scene titles, monster abilities and actor names.
- Uses DeepL for accurate translations according to the glossary.

## Workflow
1. Reads JSON file.
2. Extracts strings for translation.
3. Saves them to `work/< JSON name>_extracted.json`.
4. **First checkpoint:** decides whether to start translation.
5. Checks if there are translated strings in the translation buffer.
6. If there is a translation in the buffer, uses it; otherwise translates the missing lines via DeepL and updates the buffer file with the new data.
7. **Second checkpoint:** decides whether to generate a JSON file of the translation adventure.
8. Forming the JSON file of the adventure.

##How to use
### Download the archive DeepLAdvTranslate.rar
And unzip it to any convenient place.
https://github.com/Shadowheg/Adventure_auto_translate/releases

### Obtain API key for DeepL
1. Register at DeepL and get API key.
2. In the config.json file, replace the api_key value with your personal API key from DeepL.

### Set up and run the script
1. In the working folder, save the required glossary. In `config.json`, specify the glossary name in `DeepL_glossary_name`.
2. Register the glossary in DeepL using `CreateDeepL_Glossary.bat`. This will populate the `glossary_id` field.
3. Specify the path to the JSON file of the adventure you want to translate, it is usually best to store it in the `originals` folder.
ATTENTION:you need to specify JSON file for FOUNDRY of adventure type. This markup is required there.
4. Run the `DeepLAdvTranslate.bat` script.