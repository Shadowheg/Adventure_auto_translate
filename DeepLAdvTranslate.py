import os
import json
import csv
import re
import deepl
import hashlib

# Загрузка конфигурации
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

api_key = config['api_key']
glossary_id = config['glossary_id']
file_path = config['file_path']
source_lang = config['source_lang']  
target_lang = config['target_lang']    
translations_cache_file = config['translations_cache_file']
file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]


# Создание экземпляра переводчика DeepL
translator = deepl.Translator(api_key)

# Подготовка директорий для результатов работы
work_dir = 'work'
result_dir = 'result'
os.makedirs(work_dir, exist_ok=True)
os.makedirs(result_dir, exist_ok=True)

# Подготовка путей к файлам до блока условия
extracted_json_file_path = os.path.join(work_dir, f"{file_name_without_extension}_journal_extracted.json")
translated_json_file_path = os.path.join(work_dir, f"{file_name_without_extension}_journal_translated.json")
translations_cache = {}
translations_cache_modified = False
translations_cache_hgits = 0
translations_cache_miss = 0
# Load the translations cache
try:
    with open(translations_cache_file, 'r', encoding='utf-8') as file:
        translations_cache = json.load(file)
except FileNotFoundError:
    print("Cache file not found, starting with an empty cache.")

def translate_text_with_deepl(text, glossary_id, target_lang, ):
    global translations_cache, translations_cache_modified, translations_cache_hgits, translations_cache_miss
    if not text:
        return text

    # Create a hash key for the text
    hash_key = hashlib.md5(text.encode('utf-8')).hexdigest()
    if hash_key in translations_cache:
        translations_cache_hgits += 1
        return translations_cache[hash_key]

    try:
        translation_options = {
            "source_lang": source_lang,
            "target_lang": target_lang,
            "tag_handling": "html" # Используем "html" для обработки HTML-тегов
        }
        if glossary_id:
            translation_options["glossary"] = glossary_id
        
        result = translator.translate_text(text, **translation_options)
        
        translations_cache[hash_key] = result.text
        translations_cache_modified = True
        translations_cache_miss += 1
        return result.text
    except Exception as e:
        print(f"Ошибка при переводе: {e}")
        return text
    
def estimate_translation_cost(translation_snippets):
    tarif = 20 / 1e6 # $20 per 1M chars
    total_length = 0
    for text in translation_snippets.values():
        if text is not None:
            total_length += len(text)
    return tarif * total_length

def extract_and_preserve(text):
    # Паттерн для поиска специального синтаксиса и отдельного захвата визуальной части в фигурных скобках
    pattern = re.compile(
        r'(@\w+\[[^\]]+\])(\{[^}]+\})?'
    )
    parts = []
    last_end = 0
    for match in pattern.finditer(text):
        start, end = match.span()
        if start > last_end:
            parts.append(text[last_end:start])  # Добавляем текст между специальными синтаксисами без изменений
        
        special_syntax = match.group(1)  # Специальный синтаксис без изменений
        visual_part = match.group(2) if match.group(2) else ''  # Визуальная часть для перевода
        
        # Оборачиваем специальный синтаксис в теги для предотвращения перевода
        parts.append(f'<span class="notranslate">{special_syntax}</span>{visual_part}')
        
        last_end = end
    if last_end < len(text):
        parts.append(text[last_end:])  # Добавляем оставшийся текст после последнего специального синтаксиса
    
    return ''.join(parts)



def extract_adventure_translation_snippets(adventure_data):
    data = {}
    # Берём название и описание приключения
    data['name'] = adventure_data['name']
    data['description'] = adventure_data['description']
# Актёры
    for actor in adventure_data.get('actors', []):
        actor_id = actor.get('_id', 'No ID')
        actor_name = extract_and_preserve(actor.get('name', ''))
        data[f'actor_{actor_id}_name'] = actor_name
        for item in actor.get('items', []):
            if item.get('type', '') == 'action':
                item_id = item.get('_id', 'No ID')
                item_name = extract_and_preserve(item.get('name', ''))
                item_description = extract_and_preserve(item.get('system', {}).get('description', {}).get('value', ''))
                data[f'actor_{actor_id}_items_{item_id}_name'] = item_name
                data[f'actor_{actor_id}_items_{item_id}_description'] = item_description
            
    # Выдираем журналы
    for journal in adventure_data['journal']:
        journal_id = journal.get('_id', 'No ID')
        if 'name' in journal:
            data[f'journal_{journal_id}_name'] = journal['name']
        for page in journal.get('pages', []):
            page_name = page.get('name', None)
            text_content = page.get('text', {}).get('content', None)
            page_id = page.get('_id', 'No Page ID')
            if text_content or page_name:
                preserved_text = extract_and_preserve(text_content) if text_content else None
                data[f'journal_{journal_id}_pages_{page_id}_name'] = page_name or None
                data[f'journal_{journal_id}_pages_{page_id}_text'] = preserved_text

        # Сцены
    for scene in adventure_data.get('scenes', []): # Предполагаем, что сцены хранятся в ключе 'scenes'
        scene_id = scene.get('_id', 'No ID')
        scene_name = scene.get('name', None)
        if scene_name:
            data[f'scene_{scene_id}_name'] = scene_name

    return data

def extract_journal_data_json(journals_data):
    data = []
    for journal in journals_data:
        for page in journal.get('pages', []):
            page_name = page.get('name', None)
            text_content = page.get('text', {}).get('content', None)
            journal_id = journal.get('_id', 'No ID')
            page_id = page.get('_id', 'No Page ID')
            if text_content or page_name:
                preserved_text = extract_and_preserve(text_content) if text_content else None
                data.append([journal_id, page_id, page_name or None, preserved_text])
    return data

def translate_and_update_adventure_data(adventure_data, translated_snippets):
    # Подставляем перевод названия и описания приключения
    adventure_data['name'] = translated_snippets.get('name', adventure_data['name'])
    adventure_data['description'] = translated_snippets.get('description', adventure_data['description'])
    # Актёры
    for actor in adventure_data['actors']:
        actor_id = actor.get('_id', 'No ID')
        if 'name' in actor:
            actor['name'] = translated_snippets.get(f'actor_{actor_id}_name', actor['name'])
        # Описания действий персонажей
        for item in actor.get('items', []):
            if 'action' != item.get('type', None):
                continue
            item_id = item.get('_id', 'No ID')
            item_name = item.get('name', None)
            item_description = item.get('system', {}).get('description', {}).get('value', None)
            if item_name:
                item['name'] = translated_snippets.get(f'actor_{actor_id}_items_{item_id}_name', item_name)
            if item_description:
                item['system']['description']['value'] = translated_snippets.get(f'actor_{actor_id}_items_{item_id}_description', item_description)
    # Расковыряли журнал, но это не всё
    for journal in adventure_data['journal']:
        journal_id = journal.get('_id', 'No ID')
        if 'name' in journal:
            journal['name'] = translated_snippets.get(f'journal_{journal_id}_name', journal['name'])
        for page in journal.get('pages', []):
            page_id = page.get('_id', None)
            text_content = page.get('text', {}).get('content', None)
            page_name = page.get('name', None)
            if text_content:
                page['text']['content'] = translated_snippets.get(f'journal_{journal_id}_pages_{page_id}_text', text_content)
            if page_name:
                page['name'] = translated_snippets.get(f'journal_{journal_id}_pages_{page_id}_name', page_name)
    #названия сцен
    for scene in adventure_data.get('scenes', []):
        scene_id = scene.get('_id', 'No ID')
        scene_name_key = f'scene_{scene_id}_name'
        if scene_name_key in translated_snippets:
            scene['name'] = translated_snippets[scene_name_key]

    # Возвращаем обновлённые данные
    return adventure_data



def extracty_snippets(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        adventure_data = json.load(file)

    translation_snippets = extract_adventure_translation_snippets(adventure_data)
 
    # Сохранение извлеченных данных
    with open(extracted_json_file_path, 'w', newline='', encoding='utf-8') as json_file:
        json.dump(translation_snippets, json_file, ensure_ascii=False, indent=4)
    
    return translation_snippets

def do_translation(translation_snippets):
    # Перевод извлеченных данных и сохранение переведенных данных
    translated_snippets = {}
    for key, text in translation_snippets.items():
        translated_text = translate_text_with_deepl(text, glossary_id)
        if translated_text is not None:  # Добавляем эту проверку
            # Очистка переведенного текста от тегов <span class="notranslate">
            cleaned_text = clean_translated_text(translated_text)
            translated_snippets[key] = cleaned_text
    with open(translated_json_file_path, 'w', newline='', encoding='utf-8') as translated_json_file:
        json.dump(translated_snippets, translated_json_file, ensure_ascii=False, indent=4)

    print(f"Извлеченные данные сохранены в файл: {extracted_json_file_path}")
    print(f"Переведенные данные сохранены в файл: {translated_json_file_path}")



def do_json_generation():
    # Проверка, существует ли переведенный файл
    if not os.path.exists(translated_json_file_path):
        print("Переведенный файл не найден. Пожалуйста, убедитесь, что перевод был выполнен или файл существует.")
        return;
    translated_snippets = {}
    # Чтение переводов из CSV
    with open(translated_json_file_path, 'r', newline='', encoding='utf-8') as json_file:
        translated_snippets = json.load(json_file)
    
    # Загрузка исходного JSON, обновление и сохранение
    with open(file_path, 'r', encoding='utf-8') as file:
        adventure_data = json.load(file)

    translate_and_update_adventure_data(adventure_data, translated_snippets)

    result_file_path = os.path.join(result_dir, f"{file_name_without_extension}_translated.json")
    with open(result_file_path, 'w', encoding='utf-8') as file:
        json.dump(adventure_data, file, ensure_ascii=False, indent=4)

    print(f"Переведенные данные сохранены в файл: {result_file_path}")

def clean_translated_text(text):
    # Удаляем теги <span class="notranslate"> и </span>, возвращая исходный специальный синтаксис
    cleaned_text = re.sub(r'<span class="notranslate">|</span>', '', text)
    return cleaned_text



# Первая часть: Извлечение и перевод
translation_snippets = extracty_snippets(file_path)
translation_cost = estimate_translation_cost(translation_snippets)
print(f'Перевод будет стоить примерно: ${format(translation_cost, ".2f")}')
shoult_do_translation = input("Делаем перевод? Y/N: ").strip().upper()
if shoult_do_translation == "Y":
    do_translation(translation_snippets)
    print(f'Переведено из кэша: {translations_cache_hgits} из deepl: {translations_cache_miss}')

# Сохраняем кэш переводов
if translations_cache_modified:
    with open(translations_cache_file, 'w', encoding='utf-8') as file:
        json.dump(translations_cache, file, ensure_ascii=False, indent=4)
    
# Вторая часть: Генерация нового JSON с подстановкой перевода
should_do_json_generation = input("Формируем JSON файл с переводом? Y/N: ").strip().upper()
if should_do_json_generation == "Y":
   do_json_generation()
else: 
    print("Выполнение завершено.")