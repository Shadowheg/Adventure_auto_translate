import deepl
import json

class DeepLCleaner:
    def __init__(self, config_path):
        self.load_config(config_path)
    
    def load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
        # Инициализация настроек из конфигурационного файла
        self.api_key = config['api_key']
        self.translator = deepl.Translator(self.api_key)
        self.glossary_name_to_delete = 'PF2e_2024_02'
    
    def delete_glossaries_by_name(self):
        """Удалить все глоссарии с заданным именем."""
        glossaries = self.translator.list_glossaries()
        for glossary in glossaries:
            if glossary.name == self.glossary_name_to_delete:
                self.translator.delete_glossary(glossary.glossary_id)  
                print(f"Глоссарий {glossary.name} ({glossary.glossary_id}) успешно удален.")

# Пример использования
# Путь к вашему конфигурационному файлу
config_path = 'config.json'
cleaner = DeepLCleaner(config_path)
cleaner.delete_glossaries_by_name()
