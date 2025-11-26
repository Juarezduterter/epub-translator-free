"""
ePub Parser Module
Handles reading, parsing, and writing ePub files while preserving structure.
"""

import os
import tempfile
from typing import List, Dict, Tuple
from ebooklib import epub
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EPubParser:
    """
    Parser for ePub files that preserves structure and metadata.
    """

    def __init__(self, epub_path: str):
        """
        Initialize the parser with an ePub file.

        Args:
            epub_path: Path to the ePub file
        """
        self.epub_path = epub_path
        self.book = None
        self.translatable_items = []

    def load(self) -> epub.EpubBook:
        """
        Load the ePub file.

        Returns:
            The loaded ePub book object
        """
        try:
            self.book = epub.read_epub(self.epub_path)
            logger.info(f"Successfully loaded ePub: {self.epub_path}")
            return self.book
        except Exception as e:
            logger.error(f"Error loading ePub: {e}")
            raise

    def extract_translatable_content(self) -> List[Dict]:
        """
        Extract all translatable content from the ePub.

        Returns:
            List of dictionaries containing item info and extractable text
        """
        if not self.book:
            self.load()

        self.translatable_items = []

        for item in self.book.get_items():
            if item.get_type() == epub.ITEM_DOCUMENT:
                content = item.get_content()
                soup = BeautifulSoup(content, 'lxml')

                # Extract all text nodes that should be translated
                text_elements = []
                for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                                          'li', 'td', 'th', 'div', 'span', 'a',
                                          'blockquote', 'em', 'strong', 'i', 'b']):
                    if tag.string and tag.string.strip():
                        text_elements.append({
                            'tag': tag.name,
                            'text': tag.string.strip(),
                            'tag_object': tag
                        })

                self.translatable_items.append({
                    'item': item,
                    'soup': soup,
                    'text_elements': text_elements,
                    'original_content': content
                })

        logger.info(f"Extracted {len(self.translatable_items)} translatable items")
        return self.translatable_items

    def get_all_texts(self) -> List[str]:
        """
        Get all translatable texts as a flat list.

        Returns:
            List of text strings to translate
        """
        if not self.translatable_items:
            self.extract_translatable_content()

        all_texts = []
        for item_data in self.translatable_items:
            for element in item_data['text_elements']:
                all_texts.append(element['text'])

        return all_texts

    def update_with_translations(self, translations: List[str]) -> None:
        """
        Update the ePub content with translated texts.

        Args:
            translations: List of translated strings in the same order as get_all_texts()
        """
        if not self.translatable_items:
            raise ValueError("No translatable items loaded. Call extract_translatable_content() first.")

        translation_index = 0

        for item_data in self.translatable_items:
            soup = item_data['soup']

            for element in item_data['text_elements']:
                if translation_index < len(translations):
                    # Replace the text with translation
                    element['tag_object'].string.replace_with(translations[translation_index])
                    translation_index += 1

            # Update the item content
            new_content = str(soup)
            item_data['item'].set_content(new_content.encode('utf-8'))

        logger.info(f"Updated {translation_index} text elements with translations")

    def save(self, output_path: str) -> None:
        """
        Save the modified ePub to a new file.

        Args:
            output_path: Path where to save the translated ePub
        """
        if not self.book:
            raise ValueError("No book loaded")

        try:
            epub.write_epub(output_path, self.book)
            logger.info(f"Successfully saved translated ePub to: {output_path}")
        except Exception as e:
            logger.error(f"Error saving ePub: {e}")
            raise

    def get_metadata(self) -> Dict:
        """
        Extract metadata from the ePub.

        Returns:
            Dictionary containing metadata
        """
        if not self.book:
            self.load()

        metadata = {
            'title': self.book.get_metadata('DC', 'title'),
            'creator': self.book.get_metadata('DC', 'creator'),
            'language': self.book.get_metadata('DC', 'language'),
            'identifier': self.book.get_metadata('DC', 'identifier'),
        }

        return metadata

    def update_metadata(self, **kwargs) -> None:
        """
        Update ePub metadata.

        Args:
            **kwargs: Metadata fields to update (title, creator, language, etc.)
        """
        if not self.book:
            raise ValueError("No book loaded")

        for key, value in kwargs.items():
            if key == 'language':
                # Update language metadata
                self.book.set_language(value)
            elif key == 'title':
                self.book.set_title(value)
