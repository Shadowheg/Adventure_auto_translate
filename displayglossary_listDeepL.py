import deepl

api_key = "<your_api_key>"

# Замените 'your_api_key' на ваш ключ API DeepL
translator = deepl.Translator(api_key)

# Получение списка глоссариев
glossaries = translator.list_glossaries()

for glossary in glossaries:
    print(f"Глоссарий: {glossary.name} ID:{glossary.glossary_id}")