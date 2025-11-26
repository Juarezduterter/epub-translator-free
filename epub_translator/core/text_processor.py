"""
Text Processing Module
Handles text chunking and batching for translation.
"""

import re
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class TextProcessor:
    """
    Handles intelligent text chunking for translation.
    """

    def __init__(self, max_length: int = 512):
        """
        Initialize the text processor.

        Args:
            max_length: Maximum length of each chunk (in characters)
        """
        self.max_length = max_length

    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.

        Args:
            text: Input text

        Returns:
            List of sentences
        """
        # Simple sentence splitting (can be improved with nltk or spacy)
        # Handle common abbreviations
        text = re.sub(r'\b(Mr|Mrs|Ms|Dr|Prof|Sr|Jr)\.\s', r'\1<DOT> ', text)

        # Split on sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text)

        # Restore abbreviations
        sentences = [s.replace('<DOT>', '.') for s in sentences]

        return [s.strip() for s in sentences if s.strip()]

    def chunk_texts(self, texts: List[str]) -> Tuple[List[str], List[int]]:
        """
        Chunk texts into smaller pieces suitable for translation.

        Args:
            texts: List of texts to chunk

        Returns:
            Tuple of (chunked_texts, mapping_indices)
            mapping_indices maps each chunk back to its original text index
        """
        chunks = []
        mapping = []

        for idx, text in enumerate(texts):
            if len(text) <= self.max_length:
                # Text is small enough, use as is
                chunks.append(text)
                mapping.append(idx)
            else:
                # Split into sentences and batch
                sentences = self.split_into_sentences(text)
                current_chunk = []
                current_length = 0

                for sentence in sentences:
                    sentence_length = len(sentence)

                    if current_length + sentence_length + 1 <= self.max_length:
                        # Add to current chunk
                        current_chunk.append(sentence)
                        current_length += sentence_length + 1
                    else:
                        # Save current chunk and start new one
                        if current_chunk:
                            chunks.append(' '.join(current_chunk))
                            mapping.append(idx)

                        # Handle very long sentences
                        if sentence_length > self.max_length:
                            # Split by words
                            words = sentence.split()
                            temp_chunk = []
                            temp_length = 0

                            for word in words:
                                word_length = len(word) + 1
                                if temp_length + word_length <= self.max_length:
                                    temp_chunk.append(word)
                                    temp_length += word_length
                                else:
                                    if temp_chunk:
                                        chunks.append(' '.join(temp_chunk))
                                        mapping.append(idx)
                                    temp_chunk = [word]
                                    temp_length = word_length

                            if temp_chunk:
                                chunks.append(' '.join(temp_chunk))
                                mapping.append(idx)

                            current_chunk = []
                            current_length = 0
                        else:
                            current_chunk = [sentence]
                            current_length = sentence_length

                # Don't forget the last chunk
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    mapping.append(idx)

        logger.info(f"Chunked {len(texts)} texts into {len(chunks)} chunks")
        return chunks, mapping

    def reconstruct_texts(self, chunks: List[str], mapping: List[int],
                         original_count: int) -> List[str]:
        """
        Reconstruct original text structure from translated chunks.

        Args:
            chunks: List of translated chunks
            mapping: Mapping indices from chunking
            original_count: Number of original texts

        Returns:
            List of reconstructed texts
        """
        reconstructed = [''] * original_count

        for chunk, idx in zip(chunks, mapping):
            if reconstructed[idx]:
                # Append with space
                reconstructed[idx] += ' ' + chunk
            else:
                reconstructed[idx] = chunk

        return reconstructed

    def batch_chunks(self, chunks: List[str], batch_size: int = 8) -> List[List[str]]:
        """
        Create batches of chunks for efficient translation.

        Args:
            chunks: List of text chunks
            batch_size: Number of chunks per batch

        Returns:
            List of batches
        """
        batches = []
        for i in range(0, len(chunks), batch_size):
            batches.append(chunks[i:i + batch_size])

        logger.info(f"Created {len(batches)} batches from {len(chunks)} chunks")
        return batches

    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text before translation.

        Args:
            text: Input text

        Returns:
            Preprocessed text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        # Strip leading/trailing whitespace
        text = text.strip()

        return text

    def postprocess_text(self, text: str) -> str:
        """
        Postprocess text after translation.

        Args:
            text: Translated text

        Returns:
            Postprocessed text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        # Fix common spacing issues around punctuation
        text = re.sub(r'\s+([,.!?;:])', r'\1', text)
        text = re.sub(r'([¿¡])\s+', r'\1', text)

        # Strip leading/trailing whitespace
        text = text.strip()

        return text
