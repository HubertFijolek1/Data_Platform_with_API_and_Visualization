from transformers import pipeline

# For demonstration, i use a simple sentiment-analysis pipeline.
sentiment_pipeline = pipeline("sentiment-analysis")


def analyze_text_sentiment(texts: list[str]) -> list:
    """
    Analyze sentiment for a list of text inputs using a BERT-based model
    provided by the 'transformers' library's pipeline.
    """
    results = sentiment_pipeline(texts)
    return results
