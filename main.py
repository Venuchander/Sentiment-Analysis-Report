import re
from textblob import TextBlob
import pandas as pd

#Load the dataset
reviews_df = pd.read_excel('user_review.xls')

#Specify the column name containing the review text
column_name = 'review'
columns_to_keep = [column_name]


reviews_df = reviews_df[columns_to_keep]
reviews_df.dropna(inplace=True)

#Perform text preprocessing
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

reviews_df[column_name] = reviews_df[column_name].apply(preprocess_text)

#Perform sentiment analysis
def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

reviews_df['sentiment'] = reviews_df[column_name].apply(get_sentiment)

#Generate summary report
sentiment_counts = reviews_df['sentiment'].value_counts(bins=[-1, -0.5, 0.5, 1])
sentiment_distribution = sentiment_counts / len(reviews_df) * 100

report = f"""
# Sentiment Analysis Report

## Dataset
Number of reviews: {len(reviews_df)}

## Sentiment Distribution
Positive reviews: {sentiment_distribution[0.5:].sum():.2f}%
Negative reviews: {sentiment_distribution[:0.5].sum():.2f}%
Neutral reviews: {sentiment_distribution[0.5:0.5].sum():.2f}%
"""

with open('Report.md', 'w') as file:
    file.write(report)