"""
NLP Pipeline - Text Classification
Multi-domain classification: finance, game, AI, robotics
"""

import re
from enum import Enum
from typing import Optional


class Domain(str, Enum):
    """Domain categories"""
    FINANCE = "finance"
    GAME = "game"
    AI = "ai"
    ROBOTICS = "robotics"
    UNKNOWN = "unknown"


# Keyword-based classification rules
DOMAIN_KEYWORDS = {
    Domain.FINANCE: [
        # Financial terms
        r'\b(stock|bond|report|earnings|revenue|profit|loss)\b',
        r'\b(market|trading|invest|portfolio|dividend)\b',
        r'\b(central bank|federal reserve|inflation|gdp)\b',
        r'\b(macro economic|finance|financial)\b',
        r'\b(quarterly|annual|sec|forex|currency)\b',
    ],
    Domain.GAME: [
        # Game dev terms
        r'\b(game|playtesting|gameplay|level design)\b',
        r'\b(unity|unreal|godot|engine)\b',
        r'\b(graphics|shader|rendering|animation)\b',
        r'\b(audio|sound effect|music|bgm)\b',
        r'\b(indie|aa|aaa|publish|steam)\b',
    ],
    Domain.AI: [
        # AI/ML terms
        r'\b(ai|artificial intelligence|machine learning)\b',
        r'\b(llm|language model|transformer|gpt)\b',
        r'\b(neural network|deep learning|model)\b',
        r'\b(prompt|token|embedding|vector)\b',
        r'\b(agent|rag|ragstack|openai|anthropic)\b',
    ],
    Domain.ROBOTICS: [
        # Robotics terms
        r'\b(robot|robotics|automation|actuator)\b',
        r'\b(sensor|imurecognition|navigation)\b',
        r'\b(ros|moveit|nav2|quadruped|bipedal)\b',
        r'\b(perception|computer vision|lidar|camera)\b',
        r'\b(control|planner|kinematics|dynamics)\b',
    ],
}


def classify_text(text: str, threshold: int = 1) -> Domain:
    """
    Classify text into domain category using keyword matching.
    
    Args:
        text: Input text to classify
        threshold: Minimum keyword matches required
        
    Returns:
        Domain category
    """
    if not text or not isinstance(text, str):
        return Domain.UNKNOWN
    
    text_lower = text.lower()
    scores = {}
    
    for domain, patterns in DOMAIN_KEYWORDS.items():
        score = 0
        for pattern in patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                score += 1
        scores[domain] = score
    
    # Find domain with highest score
    max_domain = Domain.UNKNOWN
    max_score = 0
    
    for domain, score in scores.items():
        if score > max_score:
            max_score = score
            max_domain = domain
    
    return max_domain if max_score >= threshold else Domain.UNKNOWN


def classify_with_confidence(text: str, threshold: int = 1) -> tuple[Domain, float]:
    """
    Classify text with confidence score.
    
    Returns:
        Tuple of (domain, confidence 0-1)
    """
    if not text:
        return Domain.UNKNOWN, 0.0
    
    text_lower = text.lower()
    scores = {}
    total_matches = 0
    
    for domain, patterns in DOMAIN_KEYWORDS.items():
        score = 0
        for pattern in patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                score += 1
        scores[domain] = score
        total_matches += score
    
    # Find best domain
    max_domain = Domain.UNKNOWN
    max_score = 0
    
    for domain, score in scores.items():
        if score > max_score:
            max_score = score
            max_domain = domain
    
    # Calculate confidence
    if total_matches == 0:
        return Domain.UNKNOWN, 0.0
    
    if max_score < threshold:
        return Domain.UNKNOWN, max_score / threshold * 0.5
    
    confidence = max_score / max(total_matches, 1)
    return max_domain, min(confidence, 1.0)


def get_domain_probabilities(text: str) -> dict[str, float]:
    """
    Get probability distribution across all domains.
    
    Returns:
        Dictionary mapping domain to probability
    """
    if not text:
        return {d.value: 0.0 for d in Domain}
    
    text_lower = text.lower()
    scores = {}
    total = 0
    
    for domain, patterns in DOMAIN_KEYWORDS.items():
        score = sum(1 for p in patterns if re.search(p, text_lower, re.IGNORECASE))
        scores[domain.value] = score
        total += score
    
    if total == 0:
        return {d.value: 0.0 for d in Domain}
    
    return {d: s / total for d, s in scores.items()}


# Quick test
if __name__ == "__main__":
    test_texts = [
        "The Federal Reserve announced interest rate cuts today affecting stock markets",
        "New Unity 6 engine brings improved rendering and shader pipeline",
        "GPT-4 and transformer models are revolutionizing AI applications",
        "Boston Dynamics robot navigated autonomously using computer vision",
        "Steam indie game sales exceeded expectations this quarter",
    ]
    
    for text in test_texts:
        domain, conf = classify_with_confidence(text)
        probs = get_domain_probabilities(text)
        print(f"\nText: {text[:60]}...")
        print(f"  → {domain.value} (conf: {conf:.2f})")
        print(f"  Probs: { {k: round(v, 2) for k, v in probs.items()} }")