#!/usr/bin/env python3
"""
Advanced translation example.

This demonstrates advanced features like:
- Using NLLB model for better quality
- Custom batch sizes
- GPU acceleration
- Low-level API usage
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from epub_translator import (
    translate_epub,
    EPubParser,
    Translator,
    TextProcessor,
    list_available_models
)


def example_1_high_quality():
    """Example 1: High-quality translation with NLLB."""
    print("\n" + "="*60)
    print("Example 1: High-quality translation with NLLB")
    print("="*60)

    translate_epub(
        input_path="book.epub",
        output_path="book_fr_hq.epub",
        source_lang="en",
        target_lang="fr",
        model_type="nllb",
        model_name="facebook/nllb-200-distilled-600M",
        device="cuda",  # Use GPU if available
        batch_size=16,  # Larger batch for faster processing
    )


def example_2_batch_translation():
    """Example 2: Translate multiple books."""
    print("\n" + "="*60)
    print("Example 2: Batch translation")
    print("="*60)

    books = [
        ("book1.epub", "book1_es.epub", "es"),
        ("book2.epub", "book2_de.epub", "de"),
        ("book3.epub", "book3_it.epub", "it"),
    ]

    for input_file, output_file, target_lang in books:
        if not Path(input_file).exists():
            print(f"Skipping {input_file} (not found)")
            continue

        print(f"\nTranslating {input_file} to {target_lang}...")
        translate_epub(
            input_path=input_file,
            output_path=output_file,
            source_lang="en",
            target_lang=target_lang,
            model_type="marian",
        )
        print(f"✓ Saved to {output_file}")


def example_3_lowlevel_api():
    """Example 3: Using low-level API for custom processing."""
    print("\n" + "="*60)
    print("Example 3: Low-level API")
    print("="*60)

    # Parse ePub
    parser = EPubParser("book.epub")
    parser.load()
    metadata = parser.get_metadata()

    print(f"Book metadata:")
    print(f"  Title: {metadata.get('title')}")
    print(f"  Language: {metadata.get('language')}")

    # Extract content
    parser.extract_translatable_content()
    texts = parser.get_all_texts()
    print(f"  Text elements: {len(texts)}")

    # Process texts
    processor = TextProcessor(max_length=512)
    chunks, mapping = processor.chunk_texts(texts)
    print(f"  Chunks: {len(chunks)}")

    # Translate with custom settings
    translator = Translator(
        source_lang="en",
        target_lang="fr",
        model_type="nllb",
        device="cuda",
        batch_size=32,
    )

    print(f"\nTranslating with {translator}...")
    translated_chunks = translator.translate(chunks, show_progress=True)

    # Reconstruct
    translations = processor.reconstruct_texts(
        translated_chunks, mapping, len(texts)
    )

    # Update and save
    parser.update_with_translations(translations)
    parser.update_metadata(language="fr")
    parser.save("book_custom.epub")

    print("✓ Done!")


def example_4_list_models():
    """Example 4: List available models."""
    print("\n" + "="*60)
    print("Example 4: Available models")
    print("="*60)

    list_available_models()


def main():
    """Run examples."""
    print("ePub Translator - Advanced Examples")

    # List models
    example_4_list_models()

    # Uncomment the example you want to run:

    # example_1_high_quality()
    # example_2_batch_translation()
    # example_3_lowlevel_api()

    print("\n" + "="*60)
    print("Examples complete!")
    print("Uncomment the examples you want to run in main()")
    print("="*60)


if __name__ == "__main__":
    main()
