import deepl
import csv
import json


# Загрузка конфигурации
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

api_key = config['api_key']
csv_glossary_path = config['csv_glossary_path']
glossary_name = config['DeepL_glossary_name']  
source_lang = config['source_lang']  
target_lang = config['target_lang']    


# Замените 'your_api_key' на ваш ключ API DeepL
translator = deepl.Translator(api_key)

# Чтение CSV файла и подготовка данных глоссария
entries = {} 
with open(csv_glossary_path, mode='r', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    for row in csv_reader:
        source_term = row[0]  # Термин на исходном языке
        target_term = row[1]  # Перевод термина на целевой язык
        entries[source_term] = target_term

glossary = translator.create_glossary(glossary_name, source_lang, target_lang, entries)


print(f"Глоссарий '{glossary.name}' успешно создан.")

# Получение ID только что созданного глоссария
glossaries = translator.list_glossaries()
glossary_id = None
for glossary in glossaries:
    if glossary.name == glossary_name:
        glossary_id = glossary.glossary_id
        break

if glossary_id:
    print(f"ID глоссария '{glossary_name}': {glossary_id}")
else:
    print("Глоссарий не найден.")

# Обновление config.json с новым glossary_id
if glossary_id:
    config['glossary_id'] = glossary_id
    with open('config.json', 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=4)
    print(f"Глоссарий '{glossary_name}' успешно создан и его ID ({glossary_id}) сохранен в config.json.")
else:
    print("Ошибка при сохранении ID глоссария.")