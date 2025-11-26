"""
ePub Translator - Free and Open Source ePub Translation Tool

A complete tool for translating ePub files using free HuggingFace models.
No API keys required, runs 100% locally or on Google Colab.
"""

import logging
from typing import Optional, Union
from pathlib import Path

from .core.epub_parser import EPubParser
from .core.translator import Translator, list_available_models
from .core.text_processor import TextProcessor

__version__ = "1.0.0"
__author__ = "ePub Translator Contributors"
__license__ = "MIT"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def translate_epub(
    input_path: str,
    output_path: str,
    source_lang: str,
    target_lang: str,
    model_type: str = 'marian',
    model_name: Optional[str] = None,
    device: Optional[str] = None,
    batch_size: int = 8,
    max_chunk_length: int = 512,
) -> None:
    """
    Translate an ePub file from one language to another.

    This is the main high-level API function.

    Args:
        input_path: Path to the input ePub file
        output_path: Path where to save the translated ePub
        source_lang: Source language code (e.g., 'en', 'fr', 'de')
        target_lang: Target language code (e.g., 'en', 'fr', 'de')
        model_type: Translation model type ('marian', 'm2m100', 'nllb')
        model_name: Specific model name (if None, uses default for model_type)
        device: Device to use ('cuda', 'cpu', or None for auto-detection)
        batch_size: Number of texts to translate in each batch
        max_chunk_length: Maximum length of text chunks

    Example:
        >>> translate_epub(
        ...     input_path='book.epub',
        ...     output_path='book_translated.epub',
        ...     source_lang='en',
        ...     target_lang='fr'
        ... )

    Example with specific model:
        >>> translate_epub(
        ...     input_path='book.epub',
        ...     output_path='book_translated.epub',
        ...     source_lang='en',
        ...     target_lang='fr',
        ...     model_type='nllb',
        ...     model_name='facebook/nllb-200-distilled-600M'
        ... )
    """
    logger = logging.getLogger(__name__)

    logger.info(f"Starting translation: {source_lang} -> {target_lang}")
    logger.info(f"Input: {input_path}")
    logger.info(f"Output: {output_path}")

    # Step 1: Parse the ePub
    logger.info("Step 1/4: Parsing ePub file...")
    parser = EPubParser(input_path)
    parser.load()
    parser.extract_translatable_content()

    # Step 2: Extract texts
    logger.info("Step 2/4: Extracting translatable content...")
    texts = parser.get_all_texts()
    logger.info(f"Found {len(texts)} text elements to translate")

    if not texts:
        logger.warning("No translatable content found!")
        return

    # Step 3: Process and translate
    logger.info("Step 3/4: Translating content...")

    # Initialize translator
    translator = Translator(
        source_lang=source_lang,
        target_lang=target_lang,
        model_type=model_type,
        model_name=model_name,
        device=device,
        batch_size=batch_size,
    )

    # Initialize text processor
    processor = TextProcessor(max_length=max_chunk_length)

    # Chunk texts
    chunks, mapping = processor.chunk_texts(texts)
    logger.info(f"Split into {len(chunks)} chunks for translation")

    # Translate chunks
    translated_chunks = translator.translate(chunks, show_progress=True)

    # Reconstruct original structure
    translations = processor.reconstruct_texts(
        translated_chunks, mapping, len(texts)
    )

    # Step 4: Update and save
    logger.info("Step 4/4: Updating ePub and saving...")
    parser.update_with_translations(translations)

    # Update language metadata
    parser.update_metadata(language=target_lang)

    # Save translated ePub
    parser.save(output_path)

    logger.info(f"Translation complete! Saved to: {output_path}")


# Export public API
__all__ = [
    'translate_epub',
    'EPubParser',
    'Translator',
    'TextProcessor',
    'list_available_models',
]
