# Examples

This directory contains example scripts demonstrating various features of the ePub Translator.

## Files

### `simple_translation.py`

Basic translation example showing minimal setup:
- Load an ePub file
- Translate using MarianMT
- Save the result

Usage:
```bash
python simple_translation.py
```

### `advanced_translation.py`

Advanced examples demonstrating:
- High-quality translation with NLLB
- Batch translation of multiple books
- Low-level API usage
- Listing available models

Usage:
```bash
python advanced_translation.py
```

## Quick Start

1. Place an ePub file in this directory or specify the path
2. Edit the example scripts to set your source and target languages
3. Run the scripts:

```bash
# Simple example
python simple_translation.py

# Advanced examples
python advanced_translation.py
```

## Sample Code

### Simple Translation

```python
from epub_translator import translate_epub

translate_epub(
    input_path='book.epub',
    output_path='book_fr.epub',
    source_lang='en',
    target_lang='fr'
)
```

### Using NLLB for Better Quality

```python
translate_epub(
    input_path='book.epub',
    output_path='book_fr.epub',
    source_lang='en',
    target_lang='fr',
    model_type='nllb',
    device='cuda'
)
```

### Low-Level API

```python
from epub_translator import EPubParser, Translator, TextProcessor

# Parse
parser = EPubParser('book.epub')
parser.load()
texts = parser.get_all_texts()

# Translate
translator = Translator(source_lang='en', target_lang='fr')
translations = translator.translate(texts)

# Save
parser.update_with_translations(translations)
parser.save('output.epub')
```
