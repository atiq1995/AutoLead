"""
AUTOLEADAI - Spam Detection Module
Machine learning-based spam call detection
Author: Haider Asif & Aima Asghar

TODO: Increase training dataset (currently only 30 samples)
TODO: Experiment with other classifiers (tried SVM, RF works better)
TODO: Add online learning to improve model over time
"""
import numpy as np
import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import logging
from pathlib import Path
from typing import Dict, Tuple
import config

# Setup logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)


class SpamDetector:
    """
    ML-based spam call detector
    Classifies calls as spam or legitimate based on transcript content
    """
    
    def __init__(self):
        """Initialize spam detector"""
        self.model = None
        self.vectorizer = None
        self.threshold = config.SPAM_THRESHOLD
        self.is_trained = False
        self.keyword_boost_keywords = set()
        
        # Try to load existing model
        self._load_model()
        # Load keyword boosts (from repo blacklist if present)
        self._load_keyword_boosts()
    
    def _load_model(self):
        """Load pre-trained model if available"""
        model_path = Path(config.SPAM_MODEL_PATH)
        vectorizer_path = Path(config.SPAM_VECTORIZER_PATH)
        
        if model_path.exists() and vectorizer_path.exists():
            try:
                self.model = joblib.load(model_path)
                self.vectorizer = joblib.load(vectorizer_path)
                self.is_trained = True
                logger.info("Loaded pre-trained spam detection model")
            except Exception as e:
                logger.warning(f"Failed to load model: {e}")
                self._initialize_default_model()
        else:
            self._initialize_default_model()
    
    def _initialize_default_model(self):
        """Initialize and train a default model with sample data"""
        logger.info("Training default spam detection model...")
        
        # Sample training data (in production, use real dataset)
        spam_examples = [
            "congratulations you won a free prize call now",
            "claim your free gift card today limited time offer",
            "you have been selected for a special promotion",
            "urgent your account will be suspended",
            "free money making opportunity act now",
            "you won the lottery claim your prize",
            "limited time offer buy now get discount",
            "your computer has virus call tech support",
            "congratulations winner call to claim reward",
            "free vacation package call immediately",
            "reduce debt consolidate loans now",
            "make money from home easy opportunity",
            "final notice your warranty is expiring",
            "IRS tax refund pending claim now",
            "social security number suspended urgent action"
        ]
        
        legitimate_examples = [
            "hello i am interested in your real estate listing",
            "i would like to schedule a property viewing",
            "can you tell me more about the apartment details",
            "what is the price range for this property",
            "i am looking for a two bedroom apartment",
            "is the property still available for rent",
            "i saw your advertisement and want more information",
            "could you provide the location details",
            "i am interested in buying a house",
            "what are the payment options available",
            "i would like to speak with an agent",
            "can we arrange a meeting to discuss",
            "i need help finding a property",
            "what areas do you cover for real estate",
            "i am a serious buyer looking for property"
        ]
        
        # Create dataset
        texts = spam_examples + legitimate_examples
        labels = [1] * len(spam_examples) + [0] * len(legitimate_examples)
        
        # Train model
        self.train(texts, labels)

    def _load_keyword_boosts(self) -> None:
        """Load keyword list to lightly boost spam probability.

        Looks for 'Spam Filtering/blacklist.json' at repo root. Falls back to
        a few built-in phrases. The boost is applied in predict().
        """
        try:
            # repo root assumed to be two levels up from this file
            repo_root = Path(__file__).resolve().parents[1]
            bl_path = repo_root / 'Spam Filtering' / 'blacklist.json'
            base_keywords = {
                'free offer',
                'free prize',
                'free gift',
                'win cash',
                'free vacation',
            }
            loaded_keywords = set()
            if bl_path.exists():
                try:
                    data = json.loads(bl_path.read_text(encoding='utf-8'))
                    kws = data.get('keywords', []) if isinstance(data, dict) else []
                    for kw in kws:
                        if isinstance(kw, str) and kw.strip():
                            loaded_keywords.add(kw.strip().lower())
                except Exception:
                    pass
            self.keyword_boost_keywords = base_keywords | loaded_keywords
        except Exception:
            # Non-fatal; proceed without keyword boosts
            self.keyword_boost_keywords = set()
    
    def train(self, texts: list, labels: list):
        """
        Train the spam detection model
        
        Args:
            texts: List of text samples
            labels: List of labels (1 for spam, 0 for legitimate)
        """
        try:
            logger.info(f"Training spam detector with {len(texts)} samples...")
            
            # Create vectorizer
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            # Vectorize texts
            X = self.vectorizer.fit_transform(texts)
            y = np.array(labels)
            
            # Train Random Forest classifier
            # Haider tested SVM and Neural Networks but RF gave best results for small dataset
            self.model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10
            )
            self.model.fit(X, y)
            
            self.is_trained = True
            
            # Save model
            self._save_model()
            
            logger.info("Spam detector trained successfully")
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            raise
    
    def _save_model(self):
        """Save trained model to disk"""
        try:
            Path(config.SPAM_MODEL_PATH).parent.mkdir(parents=True, exist_ok=True)
            joblib.dump(self.model, config.SPAM_MODEL_PATH)
            joblib.dump(self.vectorizer, config.SPAM_VECTORIZER_PATH)
            logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
    
    def predict(self, text: str) -> Dict:
        """
        Predict if text is spam
        
        Args:
            text: Transcript text to analyze
        
        Returns:
            Dictionary with prediction results
        """
        if not self.is_trained:
            logger.warning("Model not trained, using default classification")
            return {
                'is_spam': False,
                'confidence': 0.0,
                'spam_probability': 0.0
            }
        
        try:
            text_lower = text.lower()
            # Vectorize input
            X = self.vectorizer.transform([text_lower])

            # Base probability from model
            spam_prob = float(self.model.predict_proba(X)[0][1])

            # Lightweight keyword-based boost for phrases like "free offer"
            boost = 0.0
            try:
                if any(kw in text_lower for kw in self.keyword_boost_keywords):
                    boost += 0.15
                # Additional minor boost when both words appear separately
                if ('free' in text_lower) and ('offer' in text_lower):
                    boost += 0.05
            except Exception:
                pass

            boosted_prob = max(0.0, min(1.0, spam_prob + boost))

            # Classify with configured threshold
            is_spam = boosted_prob >= self.threshold

            result = {
                'is_spam': bool(is_spam),
                'confidence': float(boosted_prob),
                'spam_probability': float(boosted_prob),
                'legitimate_probability': float(1 - boosted_prob),
                'boost_applied': float(boost),
            }

            logger.info(
                f"Spam detection: {'SPAM' if is_spam else 'LEGITIMATE'} "
                f"(base: {spam_prob:.2%}, boost: {boost:.0%}, final: {boosted_prob:.2%})"
            )

            return result
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {
                'is_spam': False,
                'confidence': 0.0,
                'error': str(e)
            }
    
    def analyze_features(self, text: str) -> Dict:
        """
        Analyze spam indicators in text
        
        Args:
            text: Text to analyze
        
        Returns:
            Dictionary of spam features detected
        """
        text_lower = text.lower()
        
        spam_keywords = {
            'urgency': ['urgent', 'limited time', 'act now', 'immediately', 'hurry'],
            'free_offers': ['free', 'win', 'prize', 'gift', 'won'],
            'financial': ['money', 'cash', 'debt', 'loan', 'credit'],
            'suspicious': ['congratulations', 'selected', 'claim', 'reward', 'offer']
        }
        
        features = {}
        for category, keywords in spam_keywords.items():
            found = [kw for kw in keywords if kw in text_lower]
            features[category] = {
                'detected': len(found) > 0,
                'keywords': found,
                'count': len(found)
            }
        
        return features


# Singleton instance
_spam_detector_instance = None


def get_spam_detector() -> SpamDetector:
    """Get or create singleton instance of SpamDetector"""
    global _spam_detector_instance
    if _spam_detector_instance is None:
        _spam_detector_instance = SpamDetector()
    return _spam_detector_instance

