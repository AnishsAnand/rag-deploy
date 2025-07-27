from textblob import TextBlob

def analyze_sentiment(text):
    if not text or len(text.strip()) == 0:
        return "neutral"

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity >= 0.3 and subjectivity > 0.4:
        return "positive"
    elif polarity <= -0.3 and subjectivity > 0.4:
        return "negative"
    else:
        return "neutral"
