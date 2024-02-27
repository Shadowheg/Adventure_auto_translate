# Adventure Autotranslation Module for Foundry

[![ru](https://img.shields.io/badge/lang-ru-green.svg)](README.md)

This module provides auto-translation of adventure content for Foundry VTT via the DeepL API. Version 0.5 beta.

## Features

- Translates logs (content, page titles, log names), scene titles, monster abilities and actor names.
- Uses DeepL for accurate translations according to the glossary.

## Workflow

1. Reads JSON file.
2. Extracts strings for translation.
3. Saves them to `work/< JSON name>_extracted.json`.
4. **First checkpoint:** decides whether to start translation.
5. Checks if there are translated strings in the translation buffer.
6. If there is a translation in the buffer, uses it; otherwise translates the missing lines via DeepL and updates the buffer file with the new data.
7. **Second checkpoint:** decides whether to generate a JSON file of the translation adventure.
8. Forming the JSON file of the adventure.

## How to use

### Download the archive DeepLAdvTranslate.rar

And unzip it to any convenient place.
https://github.com/Shadowheg/Adventure_auto_translate/releases

### Obtain API key for DeepL

1. Register at DeepL and get API key.
2. In the config.json file, replace the api_key value with your personal API key from DeepL.

### Set up and run the script

1. In the working folder, save the required glossary. In `config.json`, specify the glossary name in `DeepL_glossary_name`.
2. Register the glossary in DeepL using `CreateDeepL_Glossary.bat`. This will populate the `glossary_id` field.
3. Specify the path to the JSON file of the adventure you want to translate, it is usually best to store it in the `originals` folder.
   ATTENTION: you need to specify JSON file for FOUNDRY of adventure type. This markup is required there.
4. Run the `DeepLAdvTranslate.bat` script.
