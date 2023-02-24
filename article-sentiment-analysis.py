import requests
from bs4 import BeautifulSoup
from newspaper import Article
from textblob import TextBlob
import nltk

nltk.download('punkt')

newslink = "https://finance.yahoo.com/news/roomvu-joins-resaas-approved-supplier-123000989.html"

# extract the article link within each <item> tag and store in a separate list
articles = []

article = Article(newslink)
article.download()
article.parse()
article.nlp()

# store the necessary data in variables
title = article.title
summary = article.summary
keywords = article.keywords
text = article.text

# run sentiment analysis on the article text
# create a Textblob object and then get the sentiment values and store them
text_blob = TextBlob(text)
polarity = text_blob.polarity
subjectivity = text_blob.subjectivity

# now we can print out the data
print('**************************************')
print(f'Title: {title}')
print(f'URL: {newslink}')
print(f'Keywords: {keywords}')
print(f'Polarity: {polarity}')
print(f'Subjectivity: {subjectivity}')
print(f'Summary: ')
print(summary)
print('**************************************')