import requests
from bs4 import BeautifulSoup
from newspaper import Article
from textblob import TextBlob
import nltk
import xlsxwriter

nltk.download('punkt')

feed = "http://rss.cnn.com/rss/cnn_world.rss"

# first make a get request to the RSS feed
response = requests.get(feed)
# collect the contents of the request
webpage = response.content
# create a BeautifulSoup object that we can then parse to extract the links and title
soup = BeautifulSoup(webpage, features='xml')

# here we find every instance of an <item> tag, collect everything inside each tag, and store them all in a list
items = soup.find_all('item')

# extract the article link within each <item> tag and store in a separate list
articles = []
for item in items:
    link = item.find('link').text
    articles.append(link)


#
# Create the Spread Sheet
#
workbook = xlsxwriter.Workbook('inputs-outputs-files/news_analysis.xlsx')
bold = workbook.add_format({'bold': True})
row = 0
SheetName = 'News_Analysis'
worksheet = workbook.add_worksheet('News_Analysis')
worksheet.write(row, 0, 'Title', bold)
worksheet.write(row, 1, 'Summary', bold)
worksheet.write(row, 2, 'Keywords', bold)
worksheet.write(row, 3, 'Text', bold)
worksheet.write(row, 4, 'Polarity', bold)
worksheet.write(row, 5, 'Subjectivity', bold)
worksheet.write(row, 6, 'Link', bold)

# extract the data from each article, perform sentiment analysis, and then print
for url in articles:
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
