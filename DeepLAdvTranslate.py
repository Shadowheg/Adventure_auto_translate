from pathlib import Path
import json
import re
import deepl
import hashlib

class TranslationManager:
    def __init__(self, config_path='config.json'):
        self.pattern = re.compile('(@\\w+\\[.*?])(\\{[^}]+\\})?')
        self.load_config(config_path)
        self.translator = deepl.Translator(self.api_key)
        self.translations_cache = {}
        self.translations_cache_modified = False
        self.translations_cache_hits = 0
        self.translations_cache_miss = 0
        self.load_translations_cache()
        self.prepare_directories()
        self.last_saved_cache_state = None  


    def load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
        self.api_key = config['api_key']
        self.glossary_id = config['glossary_id']
        self.file_path = config['input_file_path']
        self.source_lang = config['source_lang']
        self.target_lang = config['target_lang']
        self.translations_cache_file = config['translations_cache_file']
        self.file_name_without_extension = Path(self.file_path).stem
        self.work_dir = 'work'
        self.result_dir = 'result'
        self.extracted_json_file_path = Path(self.work_dir) / f'{self.file_name_without_extension}_adventure_extracted.json'
        self.translated_json_file_path = Path(self.work_dir) / f'{self.file_name_without_extension}_adventure_translated.json'
        preset = config['Preset']
        self.translation_paths = config.get(f'{preset}_PathTranslated', [])
        self.normalized_paths = self.normalize_config_paths(self.translation_paths)


    # Загрузка кэша переводов
    def load_translations_cache(self):
        if Path(self.translations_cache_file).is_file():
            with open(self.translations_cache_file, 'r', encoding='utf-8') as file:
                self.translations_cache = json.load(file)
        else:
            print('Cache file not found, starting with an empty cache.')

    # Подготовка рабочих директорий
    def prepare_directories(self):
        Path(self.work_dir).mkdir(parents=True, exist_ok=True)
        Path(self.result_dir).mkdir(parents=True, exist_ok=True)
        
    # Функция перевода текста с помощью DeepL
    def translate_text_with_deepl(self, text):
        if not text:
            return text
        hash_key = hashlib.md5(text.encode('utf-8')).hexdigest()
        if hash_key in self.translations_cache:
            self.translations_cache_hits += 1
            return self.translations_cache[hash_key]
        try:
            translation_options = {
                'source_lang': self.source_lang, 
                'target_lang': self.target_lang, 
                'tag_handling': 'html'
            }
            if self.glossary_id:
                translation_options['glossary'] = self.glossary_id
            result = self.translator.translate_text(text, **translation_options)
            self.translations_cache[hash_key] = result.text
            self.translations_cache_modified = True
            self.translations_cache_miss += 1
            return result.text
        except Exception as e:
            print(f'Error during translation: {e}')
            return text
    
    # Извлечение и сохранение специальных тегов и их атрибутов
    def extract_and_preserve(self, text):
        parts = []
        last_end = 0
        for match in self.pattern.finditer(text):
            start, end = match.span()
            if start > last_end:
                parts.append(text[last_end:start])
            parts.append(f'<span class="notranslate">{match.group(1)}</span>{match.group(2) or ""}')
            last_end = end
        if last_end < len(text):
            parts.append(text[last_end:])
        return ''.join(parts)    

    # Очистка переведённого текста от специальных тегов
    def clean_translated_text(self, text):
        return re.sub('<span class="notranslate">|</span>', '', text)

    # Основная функция для обновления данных приключения с учётом переводов
    def translate_and_update_adventure_data(self, adventure_data, translated_snippets):
        # Интеграция переведенных сниппетов обратно в данные приключения
        self.reintegrate_translated_snippets(adventure_data, translated_snippets)
        return adventure_data

    

    def do_json_generation(self):
        # Check for the existence of the translated file
        if not Path(self.translated_json_file_path).exists():
            print('Translated file not found. Please ensure the translation has been performed or the file exists.')
            return
        # Load the translated snippets
        with Path(self.translated_json_file_path).open('r', encoding='utf-8') as file:
            translated_snippets = json.load(file)
        # Apply translations to the adventure data
        adventure_data = self.translate_and_update_adventure_data(json.load(Path(self.file_path).open('r', encoding='utf-8')), translated_snippets)
        # Save the results to a file
        result_file_path = Path(self.result_dir) / f'{self.file_name_without_extension}_translated.json'
        with result_file_path.open('w', encoding='utf-8') as file:
            json.dump(adventure_data, file, ensure_ascii=False, indent=4)
        print(f'Translated data saved to file: {result_file_path}')

    # Расчет стоимости перевода на основе количества символов
    def estimate_translation_cost(self, translation_snippets):
        tariff = 20 / 1_000_000  # Пример тарифа: $20 за 1 миллион символов
        total_length = sum(len(text) for text in translation_snippets.values() if text)
        cost = tariff * total_length
        return total_length, cost

        
    # Извлечение сниппетов для перевода из JSON файла
    def extract_snippets(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            adventure_data = json.load(file)
        snippets = self.extract_from_path(adventure_data, self.normalized_paths)
        with open(self.extracted_json_file_path, 'w', encoding='utf-8') as f:
            json.dump(snippets, f, indent=4, ensure_ascii=False)
        return snippets



    def do_translation(self, translation_snippets):
        translated_snippets = {}
        total_snippets = len(translation_snippets)
        translated_count = 0
        last_saved_percentage = -10
        for key, text in translation_snippets.items():
            # Пропускаем пустые строки
            if not text.strip():
                translated_snippets[key] = text  # Сохраняем пустой текст как есть
                continue
            # Экранируем специальные символы
            preserved_text = self.extract_and_preserve(text)
            translated_text = self.translate_text_with_deepl(preserved_text)
            # Очищаем переведенный текст от специальных тегов
            cleaned_text = self.clean_translated_text(translated_text) if translated_text != preserved_text else text
            translated_snippets[key] = cleaned_text
            self.translations_cache_modified = True
            translated_count += 1
            current_percentage = int((translated_count / total_snippets) * 100) 
            # Обновляем прогресс перевода, только если процент изменился
            if current_percentage > last_saved_percentage:
                if current_percentage % 10 == 0 and current_percentage != 0:
                    # Сохраняем кеш и выводим сообщение только на кратных 10% значениях
                    self.save_translations_cache()
                    print(f'\rTranslation progress: {current_percentage}% ({translated_count}/{total_snippets}) - Cache saved at {current_percentage}% progress.', end='')
                else:
                    print(f'\rTranslation progress: {current_percentage}% ({translated_count}/{total_snippets})', end='')
                last_saved_percentage = current_percentage
        print('\nTranslation completed.')
        if self.translations_cache_modified:
            self.save_translations_cache()
            print('Final cache saved.')
        # Сохраняем переведенные сниппеты в файл
        with self.translated_json_file_path.open('w', encoding='utf-8') as file:
            json.dump(translated_snippets, file, ensure_ascii=False, indent=4)
        print(f'Translated data saved to file: {self.translated_json_file_path}')

    def save_translations_cache(self):
        """Saves the translations cache to a file if there were changes since the last save."""
        current_cache_state = hashlib.md5(json.dumps(self.translations_cache, sort_keys=True).encode('utf-8')).hexdigest()
        if self.translations_cache_modified and current_cache_state != self.last_saved_cache_state:
            with open(self.translations_cache_file, 'w', encoding='utf-8') as file:
                json.dump(self.translations_cache, file, ensure_ascii=False, indent=4)
            self.translations_cache_modified = False
            self.last_saved_cache_state = current_cache_state  # Обновляем состояние после сохранения
            print('Translations cache saved.')

    def extract_from_path(self, data, valid_paths):
        snippets = {}
        def recurse(data, current_path='', ids=None):
            ids = ids or {}
            if isinstance(data, dict):
                for key, value in data.items():
                    new_path = f"{current_path}.{key}" if current_path else key
                    temp_path = new_path.replace('{key}', key) if '{key}' in current_path else new_path
                    if self.match_path(temp_path, valid_paths):
                        id_path = self.generate_id_path(temp_path, ids)
                        snippets[id_path] = value
                    else:
                        recurse(value, new_path, dict(ids))
            elif isinstance(data, list):
                for index, item in enumerate(data):
                    new_path = f"{current_path}[{index}]"
                    recurse(item, new_path, dict(ids))

        recurse(data)
        return snippets

    def normalize_config_paths(self, translation_paths):
        normalized_paths = []
        for path in translation_paths:
            normalized_path = path.replace("JSON.", "")  # Correctly remove "JSON." first
            normalized_path = normalized_path.replace('.[].', '.{index}.').replace('[]', '{index}')
            normalized_path = normalized_path.replace('{}', '{key}')
            normalized_paths.append(normalized_path)
        return normalized_paths


    def match_path(self, current_path, normalized_paths):
        for path in normalized_paths:
            path_regex = re.escape(path)
            path_regex = path_regex.replace(r'\.\{index\}', r'\[\d+\]')
            path_regex = path_regex.replace(r'\{key\}', r'[^.]+')
            path_regex = '^' + path_regex + '$'
            if re.fullmatch(path_regex, current_path):
                return True
        return False

    def generate_id_path(self, path, ids):
        parts = path.strip('.').split('.')
        result_path = []
        for part in parts:
            if '[' in part:  # Handling array indices
                key = part.split('[')[0]
                if key in ids:
                    result_path.append(f"{key}_{ids[key]}")
                else:
                    result_path.append(part)  # Fallback to indexed path if no _id is available
            elif '{}' in part:  # Handling wildcard keys
                key = part.replace('{}', '')
                if key in ids:
                    result_path.append(f"{key}_{ids[key]}")
                else:
                    result_path.append(part)
            else:
                result_path.append(part)
        return '.'.join(result_path)


    def reintegrate_translated_snippets(self, adventure_data, translated_snippets):
        for flat_key, translated_value in translated_snippets.items():
            parts = flat_key.split('.')
            current_data = adventure_data

            for i, part in enumerate(parts):
                # Handling list indices in keys like 'journal[0]' or 'pages[0]'
                if '[' in part and ']' in part:
                    key, index = part[:-1].split('[')  # Split 'journal[0]' into 'journal' and '0'
                    index = int(index)  # Convert index to integer

                    # Ensure current_data[key] is a list and is long enough
                    if key not in current_data:
                        current_data[key] = []  # Initialize if not exists
                    while len(current_data[key]) <= index:
                        current_data[key].append({})  # Expand list if not long enough

                    if i == len(parts) - 1:
                        current_data[key][index] = translated_value  # Set value if it's the last part
                    else:
                        current_data = current_data[key][index]  # Navigate deeper otherwise

                else:
                    if i == len(parts) - 1:
                        current_data[part] = translated_value  # Set value if it's the last part
                    else:
                        # Initialize a dictionary if not exists
                        if part not in current_data:
                            current_data[part] = {}
                        current_data = current_data[part]  # Navigate deeper into the dictionary


    def run_translation_process(self):
        # Использование значения file_path из конфигурации, загруженной в self.file_path
        file_path = self.file_path
        translated_snippets = self.extract_snippets(file_path)
        total_length, translation_cost = self.estimate_translation_cost(translated_snippets)
        print(f"Общее количество символов для перевода: {total_length}, перевод будет стоить примерно: ${format(translation_cost, '.2f')}")

        shoult_do_translation = input('Делаем перевод? Y/N: ').strip().upper()
        if shoult_do_translation == 'Y':
            self.do_translation(translated_snippets)
            print(f'Переведено из кэша: {self.translations_cache_hits} из deepl: {self.translations_cache_miss}')

        if self.translations_cache_modified:
            with open(self.translations_cache_file, 'w', encoding='utf-8') as file:
                json.dump(self.translations_cache, file, ensure_ascii=False, indent=4)

        should_do_json_generation = input('Формируем JSON файл с переводом? Y/N: ').strip().upper()
        if should_do_json_generation == 'Y':
            self.do_json_generation()
        else:
            print('Выполнение завершено.')

if __name__ == "__main__":
    # Создание экземпляра класса TranslationManager с указанием пути к файлу конфигурации
    # Предполагается, что в config.json уже указан путь к файлу для перевода
    manager = TranslationManager(config_path='config.json')
    
    # Запуск процесса перевода, используя конфигурацию и файл данных, указанные в config.json
    manager.run_translation_process()
