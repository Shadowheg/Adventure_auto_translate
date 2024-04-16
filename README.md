# Модуль автоматических переводов JSON файлов

[![en](https://img.shields.io/badge/lang-en-yellow.svg)](README.en.md)

Этот модуль обеспечивает автоперевод JSON файлов по указанным путям, изначально создавался как модуль перевода контента приключений для Foundry VTT через API DeepL. Версия 0.9 beta

## Особенности

- Работает с указанными путями в config`е для JSON файла. 
- Экранирует HTML разметку от вмешательства программы перевода для сохранения разметки и кнопок.
- Поддерживает вложенные [] и {} 
- Использует DeepL для точных переводов + поддержка глоссария.
- Пути можно вбивать пресетами для разных структур JSON файлов. 
- Переведенные строчки сохраняет в кеш перевода для экономии будущих переводов.

## Процесс работы

1. Читает JSON файл.
2. Извлекает указанные в config <preset_name>_PathTranslated строки для перевода 
3. Сохраняет их в `work/<имя JSON>_extracted.json`.
4. **Первая контрольная точка:** решение о начале перевода.
5. Проверяет наличие перевода строк в буфере перевода.
6. Если перевод есть в буфере, использует его; в противном случае переводит недостающие строки через DeepL и обновляет файл буфера новыми данными. Переведенные строки сохраняются в `work/<имя JSON>_translated.json`
7. **Вторая контрольная точка:** решение о формировании JSON файла приключения с переводом.
8. Формирование JSON файла приключения. в `result/<имя JSON>_translated.json`собираются данные из оригинального JSON файла и переведенные строки.

## Как использовать

### Скачайте архив DeepLAdvTranslate.rar

Распакуйте в любое удобное место
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

## Как перевести приключение для Foundry

### Перевод компендиума приключения.

Для успешного перевода приключения сначала нужно перевести компендиум  из игровой системы foundry. Можно извлечь с помощью babele-translation-file-generation (когда нибудь сделаю нормальный форк). Без этого не переведутся способности актеров.

### Подставить переведенный json компендиума в модуль перевода игровой системы на ваш язык.
Чаще всего игровые системы переводят модулем на основе работы модуля babele. Ваш переведенный компендиум нужно подставить в один из таких модулей. Для RU зоны это модуль PF2e Russian Translation | Русский перевод Pathfinder 2 https://gitlab.com/gnuraco/pf2r  

### Перевести само приключение
Извлечь приключение из Foundry в JSON файл. Это можно сделать с помощью FVTTDB. После перевода подставить файлы обработно.

### Экспортировать ваше приключение в игровой мир.
Проверить что у актеров перевелись абилки. 