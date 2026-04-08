"""
NLP Pipeline - Unified Pipeline
Combines classification, sentiment, and embeddings
"""

from dataclasses import dataclass
from typing import Optional, List
import json

from text_classifier import Domain, classify_text, classify_with_confidence
from sentiment import Sentiment, analyze_sentiment, get_sentiment_score
from embeddings import Embedder


@dataclass
class NLPResult:
    """NLP processing result"""
    text: str
    domain: str
    domain_confidence: float
    sentiment: str
    sentiment_score: float
    embedding: list = None


class NLPPipeline:
    """
    Unified NLP pipeline for text processing.
    """
    
    def __init__(
        self,
        embedder_dimension: int = 384,
        include_embeddings: bool = True,
    ):
        """
        Initialize NLP pipeline.
        
        Args:
            embedder_dimension: Embedding dimension
            include_embeddings: Whether to compute embeddings
        """
        self.include_embeddings = include_embeddings
        self.embedder = None
        
        if include_embeddings:
            self.embedder = Embedder(
                dimension=embedder_dimension,
            )
    
    def process(self, text: str) -> NLPResult:
        """
        Process a single text.
        
        Args:
            text: Input text
            
        Returns:
            NLPResult with all analysis
        """
        # Domain classification
        domain, confidence = classify_with_confidence(text)
        
        # Sentiment analysis
        sentiment = analyze_sentiment(text, domain.value)
        sentiment_score = get_sentiment_score(text, domain.value)
        
        # Embedding
        embedding = None
        if self.embedder:
            emb = self.embedder.encode(text)
            # Flatten 2D to 1D
            embedding = emb.flatten().tolist()
        
        return NLPResult(
            text=text[:100] + "..." if len(text) > 100 else text,
            domain=domain.value,
            domain_confidence=confidence,
            sentiment=sentiment.value,
            sentiment_score=sentiment_score,
            embedding=embedding,
        )
    
    def process_batch(self, texts: List[str]) -> List[NLPResult]:
        """
        Process multiple texts.
        
        Args:
            texts: List of input texts
            
        Returns:
            List of NLPResults
        """
        results = []
        
        for text in texts:
            result = self.process(text)
            results.append(result)
        
        return results
    
    def to_dict(self, result: NLPResult) -> dict:
        """Convert result to dictionary."""
        return {
            "text": result.text,
            "domain": result.domain,
            "confidence": result.domain_confidence,
            "sentiment": result.sentiment,
            "sentiment_score": result.sentiment_score,
            "embedding": result.embedding,
        }
    
    def to_json(self, result: NLPResult) -> str:
        """Convert result to JSON string."""
        return json.dumps(self.to_dict(result), indent=2)


def process_text(text: str) -> NLPResult:
    """
    Convenience function to process a single text.
    
    Args:
        text: Input text
        
    Returns:
        NLPResult
    """
    pipeline = NLPPipeline()
    return pipeline.process(text)


# Test
if __name__ == "__main__":
    print("NLP Pipeline Test")
    print("-" * 50)
    
    pipeline = NLPPipeline()
    
    test_texts = [
        "Federal Reserve considering interest rate cuts amid market volatility",
        "New Unity game engine brings amazing graphics improvements",
        "GPT-4 model shows remarkable language understanding capabilities",
        "Robot successfully navigated using SLAM and computer vision",
    ]
    
    for text in test_texts:
        result = pipeline.process(text)
        print(f"\nText: {text}")
        print(f"  Domain: {result.domain} ({result.domain_confidence:.2f})")
        print(f"  Sentiment: {result.sentiment} ({result.sentiment_score:.2f})")
        if result.embedding:
            print(f"  Embedding: {len(result.embedding)}D")