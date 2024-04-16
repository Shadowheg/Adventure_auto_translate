# Autotranslate JSON  for Foundry

[![en](https://img.shields.io/badge/lang-en-yellow.svg)](README.en.md)

This module provides auto-translation of JSON files to specified paths, originally created as an adventure content translation module for Foundry VTT via the DeepL API. Version 0.9 beta

## Features

- Works with specified paths in config` for JSON file. 
- Shields HTML markup from translation programme interference to preserve markup and buttons.
- Supports nested [] and {} 
- Uses DeepL for accurate translations + glossary support.
- Paths can be entered with presets for different JSON file structures. 
- Saves translated lines to translation cache to save future translations.

## Workflow

1. Reads JSON file.
2. retrieves strings specified in config <preset_name>_PathTranslated for translation 
3. Saves them to `work/<preset_name JSON>_extracted.json`.
4. **First checkpoint:** decision to start translation.
5. Checks if there are translated strings in the translation buffer.
6. If there is a translation in the buffer, uses it; otherwise translates the missing lines via DeepL and updates the buffer file with the new data. The translated lines are stored in `work/<JSON name>_translated.json`.
7. **Second checkpoint:** the decision to generate a JSON file of the translation adventure.
8. Formation of the JSON file of the adventure. the `result/<JSON name>_translated.json` collects the data from the original JSON file and the translated strings.

## How to use

### Download the archive DeepLAdvTranslate.rar

Extract it to any convenient place
https://github.com/Shadowheg/Adventure_auto_translate/releases

### Obtain API key for DeepL

1. Register at DeepL and get API key.
2. In the config.json file, replace the api_key value with your personal API key from DeepL.

### Set up and run the script

1. In the working folder, save the required glossary. In `config.json`, specify the glossary name in `DeepL_glossary_name`.
2. Register the glossary in DeepL using `CreateDeepL_Glossary.bat`. +This will populate the `glossary_id` field.
3. Specify the path to the JSON file of the adventure you want to translate, it is usually best to store it in the `originals` folder.
NOTE:you must specify the JSON file for FOUNDRY of adventure type. That is the exact markup required there.
4. Run the `DeepLAdvTranslate.bat` script.


## Supported languages/supported language

- DE (German)
- EN (English)
- ES (Spanish)
- FR (French)
- IT (Italian)
- JA (Japanese)
- NL (Dutch)
- PL (Polish)
- PT (Portuguese)
- RU (Russian)
- ZH (Chinese)

### How to translate an adventure for Foundry

### Translating a compendium adventure.

To successfully translate an adventure, you must first translate the compendium from the foundry game system. This can be extracted with babele-translation-file-generation (I'll make a normal fork someday). Without this, the actor abilities won't translate.

### Substitute the translated json of the compendium into the translation module of the game system in your language.
Most often game systems are translated by a module based on the babele module. Your translated compendium should be substituted into one of such modules. For the RU zone this is the PF2e Russian Translation module | Russian translation of Pathfinder 2 https://gitlab.com/gnuraco/pf2r.  

### Translate the adventure itself
Extract the adventure from Foundry into a JSON file. This can be done with FVTTDB. After the translation, substitute the files with the processed files.

### Export your adventure to the game world.
Verify that the actors have translated their abilites. 