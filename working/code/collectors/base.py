"""Base collector class for knowledge collection."""
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseCollector(ABC):
    """Abstract base class for all collectors."""

    def __init__(self):
        self.last_fetch: Optional[datetime] = None
        self.data: List[Dict[str, Any]] = []

    @abstractmethod
    def fetch(self, **kwargs) -> List[Dict[str, Any]]:
        """Fetch data from the source. Must be implemented by subclasses."""
        pass

    def save_to_json(self, filepath: str) -> None:
        """Save collected data to JSON file."""
        import json
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'source': self.__class__.__name__,
                'data': self.data
            }, f, ensure_ascii=False, indent=2)
        logger.info(f"Data saved to {filepath}")

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of collected data."""
        return {
            'source': self.__class__.__name__,
            'count': len(self.data),
            'last_fetch': self.last_fetch.isoformat() if self.last_fetch else None
        }