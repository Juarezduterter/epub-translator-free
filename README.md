# ePub Translator Free 📚🌍

**100% Free, 100% Open Source ePub Translation Tool**

Translate entire ePub books using powerful, free HuggingFace models. No API keys, no paid services, runs completely locally or on Google Colab with GPU acceleration.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/epub-translator-free/blob/main/notebooks/epub_translator_demo.ipynb)

## ✨ Features

- 🆓 **100% Free** - No API keys, no paid services
- 🔓 **Open Source** - MIT licensed, use anywhere
- 🚀 **Multiple Models** - Support for MarianMT, NLLB, M2M100
- 🌍 **200+ Languages** - With NLLB model
- 💻 **Local & Cloud** - Run on your machine or Google Colab
- 🎯 **Structure Preserved** - Maintains chapters, formatting, table of contents
- ⚡ **GPU Acceleration** - CUDA support for faster translation
- 🔄 **Smart Chunking** - Intelligent text segmentation
- 📦 **Easy to Use** - Simple CLI and Python API

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/epub-translator-free.git
cd epub-translator-free

# Install dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

### Basic Usage

#### Command Line

```bash
# Translate English to French
python translate.py --input book.epub --src en --tgt fr --output book_fr.epub

# Use NLLB model for better quality
python translate.py --input book.epub --src en --tgt fr --model nllb

# Use GPU acceleration
python translate.py --input book.epub --src en --tgt de --device cuda
```

#### Python API

```python
from epub_translator import translate_epub

# Simple translation
translate_epub(
    input_path='book.epub',
    output_path='book_translated.epub',
    source_lang='en',
    target_lang='fr'
)

# Advanced usage with NLLB model
translate_epub(
    input_path='book.epub',
    output_path='book_translated.epub',
    source_lang='en',
    target_lang='es',
    model_type='nllb',
    model_name='facebook/nllb-200-distilled-600M',
    device='cuda',
    batch_size=16
)
```

## 📖 Documentation

### Supported Models

| Model Type | Languages | Quality | Speed | Memory |
|------------|-----------|---------|-------|--------|
| **MarianMT** | ~50 pairs | Good | Fast | Low |
| **M2M100** | 100 languages | Very Good | Medium | Medium |
| **NLLB** | 200+ languages | Excellent | Slower | Higher |

#### Model Examples

```bash
# MarianMT (fast, efficient)
python translate.py --input book.epub --src en --tgt fr --model marian

# M2M100 (good balance)
python translate.py --input book.epub --src en --tgt es --model m2m100

# NLLB (best quality, more languages)
python translate.py --input book.epub --src en --tgt de --model nllb
```

### Supported Languages

Common language codes:
- `en` - English
- `fr` - French
- `de` - German
- `es` - Spanish
- `it` - Italian
- `pt` - Portuguese
- `nl` - Dutch
- `ru` - Russian
- `zh` - Chinese
- `ja` - Japanese
- `ar` - Arabic
- `ko` - Korean

For NLLB, 200+ languages are supported. See [NLLB language codes](https://github.com/facebookresearch/flores/blob/main/flores200/README.md#languages-in-flores-200).

### CLI Options

```bash
python translate.py --help

Options:
  --input, -i           Input ePub file path (required)
  --output, -o          Output ePub file path (default: input_translated.epub)
  --src, -s             Source language code (required)
  --tgt, -t             Target language code (required)
  --model-type          Model type: marian, m2m100, nllb (default: marian)
  --model-name          Specific model name/path (optional)
  --device              Device: cpu, cuda, auto (default: auto)
  --batch-size, -b      Batch size for translation (default: 8)
  --max-chunk-length    Maximum chunk length (default: 512)
  --list-models         List available model types
  --verbose, -v         Enable verbose logging
```

### Python API Reference

```python
from epub_translator import translate_epub, EPubParser, Translator

# High-level API
translate_epub(
    input_path: str,
    output_path: str,
    source_lang: str,
    target_lang: str,
    model_type: str = 'marian',
    model_name: Optional[str] = None,
    device: Optional[str] = None,
    batch_size: int = 8,
    max_chunk_length: int = 512,
)

# Low-level API for advanced usage
parser = EPubParser('book.epub')
parser.load()
texts = parser.get_all_texts()

translator = Translator(
    source_lang='en',
    target_lang='fr',
    model_type='nllb'
)
translations = translator.translate(texts)

parser.update_with_translations(translations)
parser.save('output.epub')
```

## 🌐 Google Colab

Run on Google Colab with free GPU:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/epub-translator-free/blob/main/notebooks/epub_translator_demo.ipynb)

```python
# In Google Colab
!git clone https://github.com/yourusername/epub-translator-free.git
%cd epub-translator-free
!pip install -r requirements.txt

from epub_translator import translate_epub
from google.colab import files

# Upload your ePub
uploaded = files.upload()
input_file = list(uploaded.keys())[0]

# Translate (uses Colab's free GPU!)
translate_epub(
    input_path=input_file,
    output_path='translated.epub',
    source_lang='en',
    target_lang='fr',
    model_type='nllb',
    device='cuda'
)

# Download result
files.download('translated.epub')
```

## 🛠️ Advanced Usage

### Custom Model

```python
# Use a specific MarianMT model
translate_epub(
    input_path='book.epub',
    output_path='book_es.epub',
    source_lang='en',
    target_lang='es',
    model_type='marian',
    model_name='Helsinki-NLP/opus-mt-en-es'
)

# Use NLLB-3.3B for best quality (requires more memory)
translate_epub(
    input_path='book.epub',
    output_path='book_fr.epub',
    source_lang='en',
    target_lang='fr',
    model_type='nllb',
    model_name='facebook/nllb-200-3.3B'
)
```

### Batch Processing

```python
import os
from epub_translator import translate_epub

books = ['book1.epub', 'book2.epub', 'book3.epub']

for book in books:
    output = f"translated_{book}"
    print(f"Translating {book}...")
    translate_epub(
        input_path=book,
        output_path=output,
        source_lang='en',
        target_lang='fr'
    )
    print(f"Done! Saved to {output}")
```

### Progress Monitoring

```python
import logging

# Enable verbose logging
logging.basicConfig(level=logging.INFO)

translate_epub(
    input_path='book.epub',
    output_path='book_fr.epub',
    source_lang='en',
    target_lang='fr'
)
```

## 📊 Performance Tips

### Speed Optimization

1. **Use GPU**: Add `--device cuda` for 5-10x speedup
2. **Increase batch size**: `--batch-size 16` (if you have enough memory)
3. **Use MarianMT**: Fastest model for common language pairs
4. **Smaller models**: Use `m2m100_418M` instead of `m2m100_1.2B`

### Memory Optimization

1. **Reduce batch size**: `--batch-size 4`
2. **Smaller models**: Use distilled versions
3. **CPU mode**: `--device cpu` (slower but uses less GPU memory)

### Quality Optimization

1. **Use NLLB**: Best translation quality
2. **Larger models**: `facebook/nllb-200-3.3B`
3. **Lower batch size**: Can improve quality slightly

## 🧪 Examples

### Example 1: Quick Translation

```bash
# Fast translation with MarianMT
python translate.py -i my_book.epub -s en -t fr -o mon_livre.epub
```

### Example 2: High Quality

```bash
# Best quality with NLLB
python translate.py -i book.epub -s en -t es \
    --model nllb \
    --model-name facebook/nllb-200-distilled-600M \
    --device cuda
```

### Example 3: Multiple Languages

```bash
# Translate to multiple languages
for lang in fr es de it; do
    python translate.py -i book.epub -s en -t $lang -o "book_${lang}.epub"
done
```

## 🔧 Troubleshooting

### Common Issues

**Out of Memory Error**
```bash
# Reduce batch size
python translate.py --input book.epub --src en --tgt fr --batch-size 2
```

**Model Download Fails**
```python
# Pre-download models
from transformers import MarianMTModel, MarianTokenizer
model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-fr")
tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-fr")
```

**Slow Translation**
```bash
# Use GPU if available
python translate.py --input book.epub --src en --tgt fr --device cuda

# Or use faster model
python translate.py --input book.epub --src en --tgt fr --model marian
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [HuggingFace](https://huggingface.co/) for providing free, open-source models
- [Helsinki-NLP](https://huggingface.co/Helsinki-NLP) for MarianMT models
- [Meta AI](https://ai.meta.com/) for NLLB and M2M100 models
- [ebooklib](https://github.com/aerkalov/ebooklib) for ePub handling

## 📧 Contact

For questions and support, please open an issue on GitHub.

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

**Made with ❤️ for the open-source community**
