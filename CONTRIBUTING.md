# Contributing to ePub Translator

Thank you for your interest in contributing to ePub Translator! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features

We welcome feature suggestions! Please open an issue with:
- Clear description of the feature
- Use cases
- Examples of how it would work

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/epub-translator-free.git
cd epub-translator-free

# Install in development mode
pip install -e .

# Install dev dependencies
pip install pytest pytest-cov
```

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions and classes
- Keep functions focused and small
- Add type hints where possible

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=epub_translator
```

### Adding New Models

To add support for a new translation model:

1. Update `epub_translator/core/translator.py`
2. Add model info to `SUPPORTED_MODELS`
3. Update language code mappings if needed
4. Add tests
5. Update documentation

## Questions?

Feel free to open an issue for any questions!

Thank you for contributing! 🙏
