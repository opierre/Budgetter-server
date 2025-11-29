from typing import Optional
from transformers import pipeline
from dashboard.models import Category
import logging

logger = logging.getLogger(__name__)

_GLOBAL_CLASSIFIER = None

class AICategorizer:
    """
    Transaction categorizer using AI (DistilBART) for zero-shot classification
    """
    
    def __init__(self, categories: list, confidence_threshold: float = 0.5):
        """
        Initialize AI categorizer
        
        Args:
            categories: List of Category objects to classify into
            confidence_threshold: Minimum confidence score to accept prediction
        """
        self.categories = categories
        self.category_names = [cat.name for cat in categories]
        self.category_map = {cat.name: cat for cat in categories}
        self.confidence_threshold = confidence_threshold
        
        # Lazy load the model
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the AI model (cached after first call)"""
        global _GLOBAL_CLASSIFIER
        if _GLOBAL_CLASSIFIER is None:
            try:
                logger.info("Loading AI model...")
                # Using zero-shot classification pipeline
                _GLOBAL_CLASSIFIER = pipeline(
                    "zero-shot-classification",
                    model="valhalla/distilbart-mnli-12-1"
                )
                logger.info("AI model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load AI model: {e}")
                _GLOBAL_CLASSIFIER = None
        
        self.classifier = _GLOBAL_CLASSIFIER
    
    def predict(self, name: str, memo: str) -> Optional[Category]:
        """
        Predict category for a transaction using AI
        
        Args:
            name: Transaction name/description
            memo: Transaction memo/note
            
        Returns:
            Category object if prediction confidence is above threshold, else None
        """
        if not self.classifier or not self.category_names:
            return None
        
        # Combine name and memo for richer context
        text = f"{name} {memo or ''}".strip()
        
        if not text:
            return None
        
        try:
            # Perform zero-shot classification
            result = self.classifier(
                text,
                candidate_labels=self.category_names,
                multi_label=False
            )
            
            # Get top prediction
            top_label = result['labels'][0]
            top_score = result['scores'][0]
            
            logger.debug(f"AI prediction: '{text}' -> {top_label} ({top_score:.2f})")
            
            # Return category if confidence is above threshold
            if top_score >= self.confidence_threshold:
                return self.category_map.get(top_label)
            
            return None
            
        except Exception as e:
            logger.error(f"Error during AI prediction: {e}")
            return None

def preload_model():
    """
    Preload the AI model into cache and memory.
    This ensures the model is downloaded and ready for use.
    """
    global _GLOBAL_CLASSIFIER
    try:
        if _GLOBAL_CLASSIFIER is None:
            logger.info("Preloading AI model...")
            _GLOBAL_CLASSIFIER = pipeline(
                "zero-shot-classification",
                model="valhalla/distilbart-mnli-12-1"
            )
            logger.info("AI model preloaded successfully")
    except Exception as e:
        logger.error(f"Failed to preload AI model: {e}")
