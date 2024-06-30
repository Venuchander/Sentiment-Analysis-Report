import re
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('vader_lexicon', quiet=True)

# Load the dataset
reviews_df = pd.read_excel('user_review.xls')

# Specify the column name containing the review text
column_name = 'review'
columns_to_keep = ['id', column_name]

reviews_df = reviews_df[columns_to_keep]
reviews_df.dropna(inplace=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Improved text preprocessing
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return ' '.join(tokens)

reviews_df['processed_review'] = reviews_df[column_name].apply(preprocess_text)

sia = SentimentIntensityAnalyzer()

# Sentiment analysis
def get_sentiment(text):
    return sia.polarity_scores(text)['compound']

reviews_df['sentiment_score'] = reviews_df['processed_review'].apply(get_sentiment)

def categorize_sentiment(score):
    if score <= -0.05:
        return 'Negative'
    else:
        return 'Positive'

reviews_df['sentiment_category'] = reviews_df['sentiment_score'].apply(categorize_sentiment)

sentiment_counts = reviews_df['sentiment_category'].value_counts()
sentiment_distribution = sentiment_counts / len(reviews_df) * 100

# Generate the md report
report = f"""
# Sentiment Analysis Report

## Dataset
Number of reviews: {len(reviews_df)}

## Sentiment Distribution
Positive reviews: {sentiment_distribution['Positive']:.2f}%  
Negative reviews: {sentiment_distribution['Negative']:.2f}%

## Top 5 Most Positive Reviews

{reviews_df.nlargest(5, 'sentiment_score')[['id', column_name]].to_markdown(index=False)}

## Top 5 Most Negative Reviews

{reviews_df.nsmallest(5, 'sentiment_score')[['id', column_name]].to_markdown(index=False)}
"""

with open('Report.md', 'w') as file:
    file.write(report)

print("Markdown report generated as 'Report.md'.")
