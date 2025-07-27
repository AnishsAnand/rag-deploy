from textblob import TextBlob

def get_sentiment(text):
    if not text.strip():
        return "neutral"
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.2:
        return "positive"
    elif polarity < -0.2:
        return "negative"
    return "neutral"
