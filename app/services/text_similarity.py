from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_text_similarity(text1: str, text2: str) -> float:
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform([text1, text2])
    return float(cosine_similarity(tfidf[0], tfidf[1])[0][0])
