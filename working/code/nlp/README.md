# NLP Pipeline - jay-knowledge-db

Multi-domain NLP processing for finance, gaming, AI, and robotics text classification.

## Features

- **Text Classification** - Keyword/regex-based domain classification (finance, game, ai, robotics)
- **Sentiment Analysis** - Lexicon-based sentiment with domain-specific modifiers
- **Embeddings** - Hash-based text embeddings with similarity computation

## Installation

```bash
cd working/code/nlp
pip install -e .
```

## Usage

```python
from nlp import process_text

# Process single text
result = process_text("Federal Reserve announced rate cuts")
print(f"Domain: {result.domain}")
print(f"Sentiment: {result.sentiment}")

# Batch processing
from nlp import NLPPipeline
pipeline = NLPPipeline()
results = pipeline.process_batch(texts)
```

## Modules

- `text_classifier.py` - Domain classification
- `sentiment.py` - Sentiment analysis
- `embeddings.py` - Text embeddings
- `pipeline.py` - Unified pipeline

## Requirements

- Python 3.8+
- numpy

## Status

🚧 Initial implementation - keyword/regex based
- Upgrade to transformers for better classification
- Add FinBERT for finance sentiment
- Add sentence-transformers for embeddings when available