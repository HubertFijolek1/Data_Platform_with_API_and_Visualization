import re
import pandas as pd
from textblob import TextBlob

class SentimentAnalyzer:
    """
    Simple demonstration of a custom sentiment analysis module
    using TextBlob for polarity analysis.
    """

    @staticmethod
    def clean_text(text: str) -> str:
        # Basic text cleaning (remove URLs, extra spaces, etc.)
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def analyze_sentiment(self, text: str) -> dict:
        """
        Returns polarity ([-1.0, 1.0]) and subjectivity ([0.0, 1.0])
        using a naive approach from TextBlob.
        """
        cleaned = self.clean_text(text)
        blob = TextBlob(cleaned)
        return {
            "polarity": blob.sentiment.polarity,
            "subjectivity": blob.sentiment.subjectivity
        }

    def batch_analyze(self, texts: list[str]) -> list[dict]:
        """
        Analyze sentiment for a list of text strings.
        Returns a list of dicts with {polarity, subjectivity}.
        """
        results = []
        for txt in texts:
            scores = self.analyze_sentiment(txt)
            results.append(scores)
        return results
