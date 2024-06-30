# Sentiment Analysis on User Reviews

This repository contains a Python script for performing sentiment analysis on user reviews. The script is designed to process an XLS file containing review text and generate a summary report that shows the distribution of positive and negative sentiments.


## Usage

1. Place your user review excel file named `user_review.xls` in the project directory.

2. Run the script:

```
   pip install -r requirements.txt 
```

## Features

- **Data Loading**: Reads user reviews from an Excel file.
- **Text Preprocessing**: 
  - Converts text to lowercase
  - Removes special characters
  - Applies lemmatization
- **Sentiment Analysis**: 
  - Uses NLTK's SentimentIntensityAnalyzer for scoring
  - Categorizes reviews as Positive or Negative
- **Report Generation**:
  - Provides an overview of the dataset
  - Calculates and displays sentiment distribution
  - Lists top 5 most positive reviews
  - Lists top 5 most negative reviews