import deepl
import json

# Загрузка конфигурации
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)
api_key = config['api_key']

# Замените 'your_api_key' на ваш ключ API DeepL
translator = deepl.Translator(api_key)

# Получение списка глоссариев
glossaries = translator.list_glossaries()

for glossary in glossaries:
    print(f"Глоссарий: {glossary.name} ID:{glossary.glossary_id}")