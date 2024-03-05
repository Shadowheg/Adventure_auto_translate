from pathlib import Path
import json
import re
import deepl
import hashlib

# Класс управления переводами
class TranslationManager:
    # Инициализация с путем к конфигурационному файлу
    def __init__(self, config_path='config.json'):
        # Регулярное выражение для поиска специальных тегов и их атрибутов
        self.pattern = re.compile('(@\\w+\\[.*?])(\\{[^}]+\\})?')
        # Загрузка конфигурации
        self.load_config(config_path)
        # Инициализация переводчика DeepL
        self.translator = deepl.Translator(self.api_key)
        # Инициализация кэша переводов
        self.translations_cache = {}
        self.translations_cache_modified = False
        self.translations_cache_hits = 0
        self.translations_cache_miss = 0
        # Загрузка кэша переводов
        self.load_translations_cache()
        # Подготовка рабочих директорий
        self.prepare_directories()

    # Загрузка конфигурации из файла
    def load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
        # Инициализация настроек из конфигурационного файла
        self.api_key = config['api_key']
        self.glossary_id = config['glossary_id']
        self.file_path = config['file_path']
        self.source_lang = config['source_lang']
        self.target_lang = config['target_lang']
        self.translations_cache_file = config['translations_cache_file']
        self.file_name_without_extension = Path(self.file_path).stem
        self.work_dir = 'work'
        self.result_dir = 'result'
        # Пути к файлам для экстракции и переведённым данным
        self.extracted_json_file_path = Path(self.work_dir) / f'{self.file_name_without_extension}_journal_extracted.json'
        self.translated_json_file_path = Path(self.work_dir) / f'{self.file_name_without_extension}_journal_translated.json'

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
        # Обновление основной информации приключения
        self.update_general_info(adventure_data, translated_snippets)
        
        # Обновление актеров и предметов
        for actor in adventure_data.get('actors', []):
            self.update_actor_and_items(actor, translated_snippets)
        
        # Обновление имен папок
        self.update_folders_names(adventure_data, translated_snippets)
        
        # Обновление имен токенов
        self.update_token_names(adventure_data, translated_snippets)
        
        # Обновление журналов и сцен
        self.update_journals_and_scenes(adventure_data, translated_snippets)
        
        return adventure_data

    
    def update_general_info(self, adventure_data, translated_snippets):
        adventure_data['name'] = translated_snippets.get('name', adventure_data.get('name', ''))
        adventure_data['description'] = translated_snippets.get('description', adventure_data.get('description', ''))    

    # Обновление данных актёров, включая их имена и детали
    def update_actor_and_items(self, actor, translated_snippets):
        actor_id = actor.get('_id', '')
        actor['name'] = translated_snippets.get(f'actors_{actor_id}_name', actor.get('name', ''))
        for detail_key in ['disable', 'description', 'reset']:
            actor_detail_key = f'actors_{actor_id}_system_details_{detail_key}'
            if actor_detail_key in translated_snippets:
                actor.setdefault('system', {}).setdefault('details', {})[detail_key] = translated_snippets[actor_detail_key]

        for item in actor.get('items', []):
            item_id = item.get('_id', '')
            item['name'] = translated_snippets.get(f'actors_{actor_id}_items_{item_id}_name', item.get('name', ''))
            item_description_key = f'actors_{actor_id}_items_{item_id}_system_description_value'
            if item_description_key in translated_snippets:
                item.setdefault('system', {}).setdefault('description', {})['value'] = translated_snippets[item_description_key]

    def update_folders_names(self, adventure_data, translated_snippets):
        if 'folders' in adventure_data:
            for folder in adventure_data['folders']:
                folder_id = folder.get('_id', '')
                folder_name_key = f'folders_{folder_id}_name'
                if folder_name_key in translated_snippets:
                    folder['name'] = translated_snippets[folder_name_key]

    def update_token_names(self, adventure_data, translated_snippets):
        if 'actors' in adventure_data:
            for actor in adventure_data['actors']:
                if 'prototypeToken' in actor:
                    token = actor['prototypeToken']
                    token_id = actor.get('_id', '')  # Используйте ID актера, если у токена нет уникального ID
                    token_name_key = f'actors_{token_id}_prototypeToken_name'
                    if token_name_key in translated_snippets:
                        token['name'] = translated_snippets[token_name_key]

    

    # Обновление названий журналов и сцен
    def update_journals_and_scenes(self, adventure_data, translated_snippets):
        # Обработка каждого журнала
        for journal in adventure_data['journal']:
            journal_id = journal.get('_id', 'No ID')
            # Обновление имени журнала
            if 'name' in journal:
                journal['name'] = translated_snippets.get(f'journal_{journal_id}_name', journal['name'])
            # Обработка страниц журнала
            for page in journal.get('pages', []):
                page_id = page.get('_id', None)
                text_content = page.get('text', {}).get('content', None)
                page_name = page.get('name', None)
                # Обновление содержания страницы
                if text_content:
                    page['text']['content'] = translated_snippets.get(f'journal_{journal_id}_pages_{page_id}_text', text_content)
                # Обновление имени страницы
                if page_name:
                    page['name'] = translated_snippets.get(f'journal_{journal_id}_pages_{page_id}_name', page_name)
        # Обработка каждой сцены
        for scene in adventure_data.get('scenes', []):
            scene_id = scene.get('_id', 'No ID')
            scene_name_key = f'scene_{scene_id}_name'
            # Обновление имени сцены, если доступен перевод
            if scene_name_key in translated_snippets:
                scene['name'] = translated_snippets[scene_name_key]
            
            # Обновление имен токенов в сцене, если доступен перевод
            for token in scene.get('tokens', []):
                token_id = token.get('_id', '')
                token_name_key = f'scene_{scene_id}_tokens_{token_id}_name'
                if token_name_key in translated_snippets:
                    token['name'] = translated_snippets[token_name_key]

            # Обновление текстов заметок в сцене, если доступен перевод
            for note in scene.get('notes', []):
                note_id = note.get('_id', '')
                note_text_key = f'scene_{scene_id}_notes_{note_id}_text'
                if note_text_key in translated_snippets:
                    note['text'] = translated_snippets[note_text_key]

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
    def extracty_snippets(self, file_path):
        try:
            adventure_data = json.load(Path(file_path).open('r', encoding='utf-8'))
            translation_snippets = self.extract_adventure_translation_snippets(adventure_data)
            # Сохранение извлеченных сниппетов в файл
            with self.extracted_json_file_path.open('w', encoding='utf-8') as file:
                json.dump(translation_snippets, file, ensure_ascii=False, indent=4)
            return translation_snippets
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}")
            return {}

    def do_translation(self, translation_snippets):
        translated_snippets = {}
        total_snippets = len(translation_snippets)
        translated_count = 0
        
        for key, text in translation_snippets.items():
            translated_text = self.translate_text_with_deepl(text)
            if translated_text != text:  # Checks if a new translation was performed.
                cleaned_text = self.clean_translated_text(translated_text)
                translated_snippets[key] = cleaned_text
                self.translations_cache_modified = True
            translated_count += 1
            print(f'\rTranslation progress: {translated_count / total_snippets * 100:.2f}% ({translated_count}/{total_snippets})', end='')
        
        print('\nTranslation completed.')  # Ensure to break the line after progress updates.
        with self.translated_json_file_path.open('w', encoding='utf-8') as file:
            json.dump(translated_snippets, file, ensure_ascii=False, indent=4)
        print(f'Extracted data saved to file: {self.extracted_json_file_path}')
        print(f'Translated data saved to file: {self.translated_json_file_path}')

    def extract_adventure_translation_snippets(self, adventure_data):
        data = {}
        # Добавляем обработку новых ключей
        data['name'] = adventure_data.get('name', '')
        data['description'] = adventure_data.get('description', '')
        
        for actor in adventure_data.get('actors', []):
            actor_id = actor.get('_id', '')
            data[f'actors_{actor_id}_name'] = actor.get('name', '')
            

            # Извлечение имени токена
            prototype_token_name = actor.get('prototypeToken', {}).get('name', '')
            if prototype_token_name:
                data[f'actors_{actor_id}_prototypeToken_name'] = self.extract_and_preserve(prototype_token_name)

            # Добавляем детали актера
            details = actor.get('system', {}).get('details', {})
            for detail_key in ['disable', 'description', 'reset']:
                data[f'actors_{actor_id}_system_details_{detail_key}'] = details.get(detail_key, '')
            
            # Обработка предметов актера
            for item in actor.get('items', []):
                item_id = item.get('_id', '')
                data[f'actors_{actor_id}_items_{item_id}_name'] = item.get('name', '')
                item_description = item.get('system', {}).get('description', {}).get('value', '')
                data[f'actors_{actor_id}_items_{item_id}_system_description_value'] = item_description

        # Extract journal names, page names, and text content
        for journal in adventure_data.get('journal', []):
            journal_id = journal.get('_id', 'No ID')
            if 'name' in journal:
                data[f'journal_{journal_id}_name'] = journal['name']
            for page in journal.get('pages', []):
                page_id = page.get('_id', 'No Page ID')
                page_name = self.extract_and_preserve(page.get('name', ''))
                text_content = self.extract_and_preserve(page.get('text', {}).get('content', ''))
                data[f'journal_{journal_id}_pages_{page_id}_name'] = page_name
                data[f'journal_{journal_id}_pages_{page_id}_text'] = text_content

        # Extract scene names
        for scene in adventure_data.get('scenes', []):
            scene_id = scene.get('_id', 'No ID')
            scene_name = self.extract_and_preserve(scene.get('name', ''))
            data[f'scene_{scene_id}_name'] = scene_name

            # Извлечение имен токенов в сценах
            for token in scene.get('tokens', []):
                token_id = token.get('_id', '')
                token_name = token.get('name', '')
                if token_name:
                    data[f'scene_{scene_id}_tokens_{token_id}_name'] = self.extract_and_preserve(token_name)

            # Извлечение заметок в сценах
            for note in scene.get('notes', []):
                note_id = note.get('_id', '')
                note_text = note.get('text', '')
                if note_text:
                    data[f'scene_{scene_id}_notes_{note_id}_text'] = self.extract_and_preserve(note_text)


        # Извлечение имен папок
        for folder in adventure_data.get('folders', []):
            folder_id = folder.get('_id', '')
            folder_name = folder.get('name', '')
            if folder_name:
                data[f'folders_{folder_id}_name'] = self.extract_and_preserve(folder_name)


        return data


    def update_item_info(self, item, actor_id, translated_snippets):
        item_id = item.get('_id', 'No ID')

        item_name_key = f'actors_{actor_id}_items_{item_id}_name'
        item['name'] = translated_snippets.get(item_name_key, item.get('name', ''))

        item_description_key = f'actors_{actor_id}_items_{item_id}_description'
        if item_description_key in translated_snippets:
            item_system_description = item.setdefault('system', {}).setdefault('description', {})
            item_system_description['value'] = translated_snippets[item_description_key]


    def update_names_with_translations(self, items, base_key, translated_snippets): # Добавлен аргумент translated_snippets
        for item in items:
            item_id = item.get('_id', 'No ID')
            name_key = f'{base_key}_{item_id}_name'
            if name_key in translated_snippets: # Используем переданный аргумент
                item['name'] = translated_snippets[name_key]
            # Дополнительная обработка для страниц журналов, если они есть
            if base_key == 'journal' and 'pages' in item:
                for page in item['pages']:
                    page_id = page.get('_id', 'No Page ID')
                    text_content_key = f'{base_key}_{item_id}_pages_{page_id}_text'
                    page_name_key = f'{base_key}_{item_id}_pages_{page_id}_name'
                    if text_content_key in translated_snippets: # Используем переданный аргумент
                        page['text']['content'] = translated_snippets[text_content_key]
                    if page_name_key in translated_snippets: # Используем переданный аргумент
                        page['name'] = translated_snippets[page_name_key]

    def run_translation_process(self):
        # Использование значения file_path из конфигурации, загруженной в self.file_path
        file_path = self.file_path
        translated_snippets = self.extracty_snippets(file_path)
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
