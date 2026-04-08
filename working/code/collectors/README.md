# Jay Knowledge DB - Knowledge Collectors

Collection modules for FR-001 Knowledge Collection.

## Structure

```
collectors/
├── __init__.py
├── macro_collector.py      # Financial macro data (power, exports, PMI)
├── arxiv_collector.py      # ArXiv paper acquisition
└── base.py                 # Base collector class
```

## Requirements

See requirements.txt for dependencies.

## Usage

```python
from collectors.macro_collector import MacroCollector
from collectors.arxiv_collector import ArxivCollector

# Fetch macro data
macro = MacroCollector()
data = macro.fetch_power_generation()

# Fetch ArXiv papers
arxiv = ArxivCollector()
papers = arxiv.search("machine learning", max_results=10)
```