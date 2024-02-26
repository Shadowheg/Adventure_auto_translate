import deepl
import json

# Загрузка конфигурации
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)
api_key = config['api_key']
glossary_name = config['DeepL_glossary_name']  

# Замените 'your_api_key' на ваш ключ API DeepL и 'PF2e_2024_02' на имя вашего глоссария
translator = deepl.Translator(api_key)


# Находим глоссарий по имени
glossary = next((g for g in translator.list_glossaries() if g.name == glossary_name), None)

if glossary:
    # Получение и печать содержимого глоссария
    entries = translator.get_glossary_entries(glossary.glossary_id)
    for source_term, target_term in entries.items():
        print(f"{source_term} -> {target_term}")
else:
    print(f"Глоссарий '{glossary_name}' не найден.")
