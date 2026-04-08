"""
NLP Pipeline - Sentiment Analysis
Basic sentiment analysis with finance-specific extensions
"""

import re
from enum import Enum
from typing import Optional


class Sentiment(str, Enum):
    """Sentiment categories"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


# Lexicon-based sentiment words
POSITIVE_WORDS = {
    # General positive
    "good", "great", "excellent", "amazing", "wonderful", "fantastic",
    "positive", "growth", "increase", "rise", "gain", "profit", "success",
    "improve", "strong", "better", "achieve", "rise", "surge", "rally",
    # Finance specific
    "bullish", "upward", "breakout", "gain", "outperform", "upgrade",
    "beat", "exceed", "growth", "profit", "dividend", "yield",
}

NEGATIVE_WORDS = {
    # General negative
    "bad", "poor", "terrible", "awful", "horrible", "negative",
    "decline", "decrease", "fall", "drop", "loss", "fail", "failure",
    "weak", "worse", "decline", "crash", "plunge", "dump",
    # Finance specific
    "bearish", "downward", "breakdown", "underperform", "downgrade",
    "miss", "deficit", "debt", "risk", "volatile", "recession",
}

# Finance-specific sentiment modifiers
FINANCE_MODIFIERS = {
    "strong": 1.5,
    "weak": -1.5,
    "beat": 1.3,
    "miss": -1.3,
    "exceed": 1.2,
    "below": -1.2,
}


def analyze_sentiment(text: str, domain: str = "general") -> Sentiment:
    """
    Analyze sentiment of text.
    
    Args:
        text: Input text
        domain: Domain (finance, game, ai, robotics)
        
    Returns:
        Sentiment category
    """
    if not text:
        return Sentiment.NEUTRAL
    
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    pos_score = sum(1 for w in words if w in POSITIVE_WORDS)
    neg_score = sum(1 for w in words if w in NEGATIVE_WORDS)
    
    # Domain-specific adjustments
    if domain == "finance":
        # Apply modifiers
        for modifier, multiplier in FINANCE_MODIFIERS.items():
            if modifier in text_lower:
                if multiplier > 0:
                    pos_score += multiplier
                else:
                    neg_score -= multiplier
    
    # Determine sentiment
    if pos_score > neg_score + 1:
        return Sentiment.POSITIVE
    elif neg_score > pos_score + 1:
        return Sentiment.NEGATIVE
    elif pos_score == neg_score:
        return Sentiment.NEUTRAL
    else:
        return Sentiment.MIXED


def get_sentiment_score(text: str, domain: str = "general") -> float:
    """
    Get numeric sentiment score (-1 to 1).
    
    Args:
        text: Input text
        domain: Domain for context-specific adjustments
        
    Returns:
        Score from -1 (negative) to +1 (positive)
    """
    if not text:
        return 0.0
    
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    pos_score = sum(1 for w in words if w in POSITIVE_WORDS)
    neg_score = sum(1 for w in words if w in NEGATIVE_WORDS)
    
    # Domain-specific adjustments
    if domain == "finance":
        for modifier, multiplier in FINANCE_MODIFIERS.items():
            if modifier in text_lower:
                if multiplier > 0:
                    pos_score += multiplier
                else:
                    neg_score -= multiplier
    
    total = pos_score + neg_score
    if total == 0:
        return 0.0
    
    return (pos_score - neg_score) / total


def get_sentiment_details(text: str, domain: str = "general") -> dict:
    """
    Get detailed sentiment analysis.
    
    Returns:
        Dictionary with sentiment info, scores, and detected words
    """
    if not text:
        return {
            "sentiment": Sentiment.NEUTRAL.value,
            "score": 0.0,
            "positive_words": [],
            "negative_words": [],
            "domain": domain,
        }
    
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    positive_words = [w for w in words if w in POSITIVE_WORDS]
    negative_words = [w for w in words if w in NEGATIVE_WORDS]
    
    pos_score = len(positive_words)
    neg_score = len(negative_words)
    
    # Domain adjustments
    if domain == "finance":
        for modifier, multiplier in FINANCE_MODIFIERS.items():
            if modifier in text_lower:
                if multiplier > 0:
                    pos_score += multiplier
                else:
                    neg_score -= multiplier
    
    total = pos_score + neg_score
    if total == 0:
        score = 0.0
    else:
        score = (pos_score - neg_score) / total
    
    # Determine sentiment
    if pos_score > neg_score + 1:
        sentiment = Sentiment.POSITIVE
    elif neg_score > pos_score + 1:
        sentiment = Sentiment.NEGATIVE
    elif pos_score == neg_score:
        sentiment = Sentiment.NEUTRAL
    else:
        sentiment = Sentiment.MIXED
    
    return {
        "sentiment": sentiment.value,
        "score": round(score, 3),
        "positive_words": positive_words,
        "negative_words": negative_words,
        "domain": domain,
    }


# Simple test
if __name__ == "__main__":
    test_texts = [
        ("Stock markets rallied today with strong gains", "finance"),
        ("Company missed earnings expectations", "finance"),
        ("Amazing game with excellent graphics", "game"),
        ("Robot navigation failed due to sensor issues", "robotics"),
        ("New AI model shows great potential", "ai"),
    ]
    
    print("Sentiment Analysis Tests:")
    print("-" * 50)
    
    for text, domain in test_texts:
        result = get_sentiment_details(text, domain)
        print(f"\nText: {text}")
        print(f"  Domain: {domain}")
        print(f"  Sentiment: {result['sentiment']} (score: {result['score']})")
        print(f"  + words: {result['positive_words']}")
        print(f"  - words: {result['negative_words']}")