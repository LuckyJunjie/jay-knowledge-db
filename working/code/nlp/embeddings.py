"""
NLP Pipeline - Text Embeddings
Basic embeddings using simple hash-based approach (fallback)
"""

import numpy as np
from typing import List, Union
from pathlib import Path
import hashlib


class Embedder:
    """
    Simple hash-based text embedder.
    Generates deterministic embeddings from text using feature hashing.
    """
    
    def __init__(
        self,
        dimension: int = 384,
    ):
        """
        Initialize embedder.
        
        Args:
            dimension: Embedding dimension
        """
        self.dimension = dimension
        
    def encode(
        self,
        texts: Union[str, List[str]],
    ) -> np.ndarray:
        """
        Encode texts to embeddings.
        
        Args:
            texts: Single text or list of texts
            
        Returns:
            Embeddings array of shape (n_texts, dimension)
        """
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = np.zeros((len(texts), self.dimension), dtype=np.float32)
        
        for i, text in enumerate(texts):
            embeddings[i] = self._text_to_embedding(text)
        
        # Normalize
        embeddings = self._normalize(embeddings)
        return embeddings
    
    def _text_to_embedding(self, text: str) -> np.ndarray:
        """Convert text to embedding vector."""
        embedding = np.zeros(self.dimension, dtype=np.float32)
        text_lower = text.lower()
        
        # Tokenize (simple whitespace + punctuation)
        tokens = text_lower.replace('.', ' ').replace(',', ' ').split()
        
        # Hash-based feature accumulation
        for token in tokens:
            # Hash token to multiple indices
            for seed in range(3):
                h = hashlib.md5(f"{token}_{seed}".encode()).hexdigest()
                idx = int(h[:8], 16) % self.dimension
                
                # Weight based on position and frequency
                embedding[idx] += 1.0 / (seed + 1)
        
        # Add sentence-level features
        embedding[int(hashlib.md5(text_lower.encode()).hexdigest()[:8], 16) % self.dimension] += len(text) / 100.0
        
        return embedding
    
    def _normalize(self, embeddings: np.ndarray) -> np.ndarray:
        """L2 normalize embeddings."""
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)
        return embeddings / norms
    
    def similarity(self, texts: List[str]) -> np.ndarray:
        """
        Compute pairwise similarity matrix.
        
        Args:
            texts: List of texts
            
        Returns:
            Similarity matrix (n x n)
        """
        embeddings = self.encode(texts)
        return np.dot(embeddings, embeddings.T)


def encode_texts(texts: List[str], dimension: int = 384) -> np.ndarray:
    """
    Convenience function to encode texts.
    
    Args:
        texts: List of texts to encode
        dimension: Embedding dimension
        
    Returns:
        Embeddings array
    """
    embedder = Embedder(dimension=dimension)
    return embedder.encode(texts)


# Test
if __name__ == "__main__":
    print("Embedder Test")
    print("-" * 50)
    
    embedder = Embedder(dimension=64)  # Use smaller for demo
    
    texts = [
        "The stock market showed strong gains today",
        "AI models are revolutionizing technology",
        "Game development requires creative skills",
        "Robot navigation uses computer vision",
        "Financial reports indicate positive growth",
    ]
    
    print("\nEncoding texts...")
    embeddings = embedder.encode(texts)
    print(f"Embeddings shape: {embeddings.shape}")
    
    # Test similarity
    print("\nSimilarity matrix (first 2 texts):")
    sim = embedder.similarity(texts[:2])
    print(np.round(sim, 2))