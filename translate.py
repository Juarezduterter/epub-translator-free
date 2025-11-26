#!/usr/bin/env python3
"""
Command-line interface for ePub Translator.

Usage:
    python translate.py --input book.epub --src en --tgt fr --output book_fr.epub
"""

import sys
import argparse
import logging
from pathlib import Path

try:
    from epub_translator import translate_epub, list_available_models
except ImportError:
    # Add current directory to path for development
    sys.path.insert(0, str(Path(__file__).parent))
    from epub_translator import translate_epub, list_available_models


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description='Translate ePub files using free HuggingFace models',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (English to French)
  python translate.py --input book.epub --src en --tgt fr --output book_fr.epub

  # Using NLLB model for better quality
  python translate.py --input book.epub --src en --tgt fr --model nllb

  # Specify custom model
  python translate.py --input book.epub --src en --tgt es \\
      --model-type marian --model-name Helsinki-NLP/opus-mt-en-es

  # Use GPU acceleration
  python translate.py --input book.epub --src en --tgt de --device cuda

  # List available models
  python translate.py --list-models

Supported Languages:
  Common codes: en, fr, de, es, it, pt, nl, ru, zh, ja, ar, ko, etc.
  For NLLB: 200+ languages supported
  For MarianMT: depends on model availability

Model Types:
  marian   - Fast and efficient (default)
  m2m100   - 100 languages, good quality
  nllb     - 200+ languages, best quality
        """
    )

    parser.add_argument(
        '--input', '-i',
        type=str,
        help='Input ePub file path'
    )

    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output ePub file path (default: input_translated.epub)'
    )

    parser.add_argument(
        '--src', '-s',
        type=str,
        help='Source language code (e.g., en, fr, de)'
    )

    parser.add_argument(
        '--tgt', '-t',
        type=str,
        help='Target language code (e.g., en, fr, de)'
    )

    parser.add_argument(
        '--model-type', '--model',
        type=str,
        default='marian',
        choices=['marian', 'm2m100', 'nllb'],
        help='Translation model type (default: marian)'
    )

    parser.add_argument(
        '--model-name',
        type=str,
        default=None,
        help='Specific model name/path (optional)'
    )

    parser.add_argument(
        '--device',
        type=str,
        default=None,
        choices=['cpu', 'cuda', 'auto'],
        help='Device to use (default: auto-detect)'
    )

    parser.add_argument(
        '--batch-size', '-b',
        type=int,
        default=8,
        help='Batch size for translation (default: 8)'
    )

    parser.add_argument(
        '--max-chunk-length',
        type=int,
        default=512,
        help='Maximum chunk length (default: 512)'
    )

    parser.add_argument(
        '--list-models',
        action='store_true',
        help='List available model types and exit'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # List models and exit
    if args.list_models:
        list_available_models()
        return 0

    # Validate required arguments
    if not args.input:
        parser.error("--input is required")
    if not args.src:
        parser.error("--src (source language) is required")
    if not args.tgt:
        parser.error("--tgt (target language) is required")

    # Set default output path
    if not args.output:
        input_path = Path(args.input)
        args.output = str(
            input_path.parent / f"{input_path.stem}_translated{input_path.suffix}"
        )

    # Validate input file
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        return 1

    # Handle device argument
    device = args.device if args.device != 'auto' else None

    # Run translation
    try:
        translate_epub(
            input_path=args.input,
            output_path=args.output,
            source_lang=args.src,
            target_lang=args.tgt,
            model_type=args.model_type,
            model_name=args.model_name,
            device=device,
            batch_size=args.batch_size,
            max_chunk_length=args.max_chunk_length,
        )
        print(f"\n✓ Translation successful!")
        print(f"  Output: {args.output}")
        return 0

    except KeyboardInterrupt:
        print("\n\nTranslation interrupted by user")
        return 130

    except Exception as e:
        print(f"\n✗ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
