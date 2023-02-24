import requests
from bs4 import BeautifulSoup
from newspaper import Article
from textblob import TextBlob
import nltk
import xlsxwriter
import csv

nltk.download('punkt')

#
# Create the Spread Sheet
#
workbook = xlsxwriter.Workbook('inputs-outputs-files/csv_news_analysis.xlsx')
bold = workbook.add_format({'bold': True})
row = 0
SheetName = 'CSV_News_Analysis'
worksheet = workbook.add_worksheet('CSV_News_Analysis')
worksheet.write(row, 0, 'Title', bold)
worksheet.write(row, 1, 'Summary', bold)
worksheet.write(row, 2, 'Keywords', bold)
worksheet.write(row, 3, 'Text', bold)
worksheet.write(row, 4, 'Polarity', bold)
worksheet.write(row, 5, 'Subjectivity', bold)
worksheet.write(row, 6, 'Link', bold)

with open("inputs-outputs-files/input_url.csv") as file:
    reader = csv.DictReader(file)

    # extract the data from each article, perform sentiment analysis, and then print
    for item in reader:
        url= item['URL']
        row += 1
        article = Article(url)
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
        print(f'URL: {url}')
        print(f'Keywords: {keywords}')
        print(f'Polarity: {polarity}')
        print(f'Subjectivity: {subjectivity}')
        print(f'Summary: ')
        print(summary)
        print(f'Text: ')
        print(text)
        print('**************************************')

        strkeywords=','.join(keywords)
        worksheet.write(row, 0,title)
        worksheet.write(row, 1,summary)
        worksheet.write(row, 2,strkeywords)
        worksheet.write(row, 3,text)
        worksheet.write(row, 4,polarity)
        worksheet.write(row, 5,subjectivity)
        worksheet.write(row, 6,url)    
workbook.close()
print("Information collected & dumped into csv")
