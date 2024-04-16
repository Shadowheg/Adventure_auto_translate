import deepl

api_key = "<your_api_key>"

# Замените 'your_api_key' на ваш ключ API DeepL и 'PF2e_2024_02' на имя вашего глоссария
translator = deepl.Translator(api_key)
glossary_name = "PF2e_2024_03"

# Находим глоссарий по имени
glossary = next((g for g in translator.list_glossaries() if g.name == glossary_name), None)

if glossary:
    # Получение и печать содержимого глоссария
    entries = translator.get_glossary_entries(glossary.glossary_id)
    for source_term, target_term in entries.items():
        print(f"{source_term} -> {target_term}")
else:
    print(f"Глоссарий '{glossary_name}' не найден.")
