#!/usr/bin/env python3
"""
Simple translation example.

This demonstrates the basic usage of the ePub translator.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from epub_translator import translate_epub


def main():
    """Run a simple translation example."""

    # Example input (you need to provide your own ePub file)
    input_file = "sample_book.epub"  # Replace with your file

    if not Path(input_file).exists():
        print(f"Error: Input file not found: {input_file}")
        print("\nPlease provide an ePub file to translate.")
        print("Usage: python simple_translation.py")
        return 1

    # Translate English to French using MarianMT
    print("Starting translation...")
    print(f"Input: {input_file}")

    translate_epub(
        input_path=input_file,
        output_path="sample_book_fr.epub",
        source_lang="en",
        target_lang="fr",
        model_type="marian",
        batch_size=8,
    )

    print("\n✓ Translation complete!")
    print("Output: sample_book_fr.epub")

    return 0


if __name__ == "__main__":
    sys.exit(main())
