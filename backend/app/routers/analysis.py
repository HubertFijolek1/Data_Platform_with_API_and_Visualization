from ..ml.bert import analyze_text_sentiment
from fastapi import HTTPException, APIRouter

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
