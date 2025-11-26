"""
Translation Module
Handles translation using various HuggingFace models.
"""

import torch
from transformers import (
    MarianMTModel,
    MarianTokenizer,
    M2M100ForConditionalGeneration,
    M2M100Tokenizer,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)
from typing import List, Optional, Union
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)


class Translator:
    """
    Translation engine supporting multiple HuggingFace models.
    """

    SUPPORTED_MODELS = {
        'marian': {
            'model_class': MarianMTModel,
            'tokenizer_class': MarianTokenizer,
            'description': 'MarianMT models (fast, good quality)',
        },
        'm2m100': {
            'model_class': M2M100ForConditionalGeneration,
            'tokenizer_class': M2M100Tokenizer,
            'description': 'M2M100 (many-to-many, 100 languages)',
        },
        'nllb': {
            'model_class': AutoModelForSeq2SeqLM,
            'tokenizer_class': AutoTokenizer,
            'description': 'NLLB (No Language Left Behind, 200+ languages)',
        },
    }

    # Language code mappings for different models
    LANGUAGE_CODES = {
        'marian': {
            'en': 'en', 'fr': 'fr', 'de': 'de', 'es': 'es', 'it': 'it',
            'pt': 'pt', 'nl': 'nl', 'ru': 'ru', 'zh': 'zh', 'ja': 'ja',
        },
        'm2m100': {
            'en': 'en', 'fr': 'fr', 'de': 'de', 'es': 'es', 'it': 'it',
            'pt': 'pt', 'nl': 'nl', 'ru': 'ru', 'zh': 'zh', 'ja': 'ja',
        },
        'nllb': {
            'en': 'eng_Latn', 'fr': 'fra_Latn', 'de': 'deu_Latn',
            'es': 'spa_Latn', 'it': 'ita_Latn', 'pt': 'por_Latn',
            'nl': 'nld_Latn', 'ru': 'rus_Cyrl', 'zh': 'zho_Hans',
            'ja': 'jpn_Jpan', 'ar': 'arb_Arab', 'ko': 'kor_Hang',
        },
    }

    def __init__(
        self,
        source_lang: str,
        target_lang: str,
        model_type: str = 'marian',
        model_name: Optional[str] = None,
        device: Optional[str] = None,
        batch_size: int = 8,
    ):
        """
        Initialize the translator.

        Args:
            source_lang: Source language code (e.g., 'en')
            target_lang: Target language code (e.g., 'fr')
            model_type: Type of model ('marian', 'm2m100', 'nllb')
            model_name: Specific model name/path (if None, uses default)
            device: Device to use ('cuda', 'cpu', or None for auto)
            batch_size: Batch size for translation
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.model_type = model_type.lower()
        self.batch_size = batch_size

        # Auto-detect device
        if device is None:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device

        logger.info(f"Using device: {self.device}")

        # Get model name
        if model_name is None:
            model_name = self._get_default_model_name()

        self.model_name = model_name
        logger.info(f"Loading model: {model_name}")

        # Load model and tokenizer
        self._load_model()

    def _get_default_model_name(self) -> str:
        """Get default model name based on model type and language pair."""
        if self.model_type == 'marian':
            # MarianMT uses specific models for each language pair
            return f"Helsinki-NLP/opus-mt-{self.source_lang}-{self.target_lang}"
        elif self.model_type == 'm2m100':
            # M2M100 has different sizes
            return "facebook/m2m100_418M"
        elif self.model_type == 'nllb':
            # NLLB has different sizes
            return "facebook/nllb-200-distilled-600M"
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def _load_model(self) -> None:
        """Load the translation model and tokenizer."""
        try:
            model_info = self.SUPPORTED_MODELS[self.model_type]
            model_class = model_info['model_class']
            tokenizer_class = model_info['tokenizer_class']

            # Load tokenizer
            self.tokenizer = tokenizer_class.from_pretrained(self.model_name)

            # Load model
            self.model = model_class.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()

            # Set source/target language for M2M100 and NLLB
            if self.model_type == 'm2m100':
                self.tokenizer.src_lang = self.source_lang
                self.tokenizer.tgt_lang = self.target_lang
            elif self.model_type == 'nllb':
                # NLLB uses special tokens
                src_code = self.LANGUAGE_CODES['nllb'].get(
                    self.source_lang, self.source_lang
                )
                tgt_code = self.LANGUAGE_CODES['nllb'].get(
                    self.target_lang, self.target_lang
                )
                self.tokenizer.src_lang = src_code
                self.tokenizer.tgt_lang = tgt_code

            logger.info(f"Model loaded successfully on {self.device}")

        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise

    def translate_batch(self, texts: List[str]) -> List[str]:
        """
        Translate a batch of texts.

        Args:
            texts: List of texts to translate

        Returns:
            List of translated texts
        """
        if not texts:
            return []

        try:
            # Tokenize
            if self.model_type == 'nllb':
                # NLLB requires forced_bos_token_id
                inputs = self.tokenizer(
                    texts,
                    return_tensors="pt",
                    padding=True,
                    truncation=True,
                    max_length=512
                ).to(self.device)

                tgt_code = self.LANGUAGE_CODES['nllb'].get(
                    self.target_lang, self.target_lang
                )
                forced_bos_token_id = self.tokenizer.convert_tokens_to_ids(tgt_code)

                with torch.no_grad():
                    translated = self.model.generate(
                        **inputs,
                        forced_bos_token_id=forced_bos_token_id,
                        max_length=512,
                        num_beams=5,
                    )
            else:
                # MarianMT and M2M100
                inputs = self.tokenizer(
                    texts,
                    return_tensors="pt",
                    padding=True,
                    truncation=True,
                    max_length=512
                ).to(self.device)

                with torch.no_grad():
                    translated = self.model.generate(
                        **inputs,
                        max_length=512,
                        num_beams=5,
                    )

            # Decode
            translations = self.tokenizer.batch_decode(
                translated, skip_special_tokens=True
            )

            return translations

        except Exception as e:
            logger.error(f"Error during translation: {e}")
            raise

    def translate(
        self,
        texts: Union[str, List[str]],
        show_progress: bool = True
    ) -> Union[str, List[str]]:
        """
        Translate text(s).

        Args:
            texts: Single text or list of texts to translate
            show_progress: Whether to show progress bar

        Returns:
            Translated text(s)
        """
        single_input = isinstance(texts, str)
        if single_input:
            texts = [texts]

        all_translations = []

        # Process in batches
        batches = [
            texts[i:i + self.batch_size]
            for i in range(0, len(texts), self.batch_size)
        ]

        iterator = tqdm(batches, desc="Translating") if show_progress else batches

        for batch in iterator:
            translations = self.translate_batch(batch)
            all_translations.extend(translations)

        if single_input:
            return all_translations[0]
        return all_translations

    def __repr__(self) -> str:
        return (
            f"Translator(model={self.model_name}, "
            f"{self.source_lang} -> {self.target_lang}, "
            f"device={self.device})"
        )


def list_available_models() -> None:
    """Print available model types."""
    print("\nAvailable model types:")
    print("-" * 60)
    for model_type, info in Translator.SUPPORTED_MODELS.items():
        print(f"{model_type:10} - {info['description']}")
    print("\nExample models:")
    print("  MarianMT:  Helsinki-NLP/opus-mt-en-fr")
    print("  M2M100:    facebook/m2m100_418M")
    print("  NLLB:      facebook/nllb-200-distilled-600M")
