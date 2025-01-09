from fastapi import APIRouter, HTTPException

from ..ml.bert import analyze_text_sentiment
from ..ml.sentiment import SentimentAnalyzer

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
)


@router.post("/bert-sentiment")
def bert_sentiment(texts: list[str]):
    """
    Example usage of the BERT pipeline for sentiment analysis.
    """
    if not texts:
        raise HTTPException(status_code=400, detail="No text provided.")
    results = analyze_text_sentiment(texts)
    return results


@router.post("/sentiment")
def sentiment_analysis(texts: list[str]):
    """
    Example usage of SentimentAnalyzer from sentiment.py.
    """
    if not texts:
        raise HTTPException(status_code=400, detail="No text provided.")

    analyzer = SentimentAnalyzer()
    results = analyzer.batch_analyze(texts)
    return results
