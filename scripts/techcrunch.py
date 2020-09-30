import requests
from bs4 import BeautifulSoup
from cleantext import clean
import re
from nltk.tokenize import RegexpTokenizer
import pandas as pd
import html


def getImageURL(text):    
    firstIndex = text.find("\"og:image\" content=")+20
    secondIndex = text.find("\"", firstIndex)
    imageURL = text[firstIndex:secondIndex]
    return imageURL

def getTokenized(text):
    firstIndex = text.find("p id=\"speakable-summary\"")+25
    secondIndex = text.find("<footer class", firstIndex)
    content = text[firstIndex:secondIndex]

    cleanr = re.compile('<.*?>')
    content = re.sub(cleanr, '', content)
    content = content.replace('\n',' ')
    content = content.replace('\t',' ')
    content = html.unescape(content)

    content = clean(content,
        fix_unicode=True,               # fix various unicode errors
        to_ascii=True,                  # transliterate to closest ASCII representation
        lower=False,                     # lowercase text
        no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
        no_urls=False,                  # replace all URLs with a special token
        no_emails=False,                # replace all email addresses with a special token
        no_phone_numbers=False,         # replace all phone numbers with a special token
        no_numbers=False,               # replace all numbers with a special token
        no_digits=False,                # replace all digits with a special token
        no_currency_symbols=False,      # replace all currency symbols with a special token
        no_punct=False,                 # fully remove punctuation
    )

    tokenizer = RegexpTokenizer(r'([%$&\-\+]?\b[^\s]+\b[%$&]?)')
    content = tokenizer.tokenize(content)

    return content

def getTechCrunch():
    response = requests.get('https://techcrunch.com/')
    soup = BeautifulSoup(response.text, 'html.parser')

    allAs = soup.find_all("a", class_='post-block__title__link')

    allRefs = []
    allTitles = []

    for each in allAs:
        allRefs.append(each['href'])
        allTitles.append(each.text)

    allNews = []
    for each in allRefs:
        response = requests.get(each)
        text = response.text
        image = getImageURL(text)
        content = getTokenized(text)
        allNews.append([each,image,content])

    allNews = pd.DataFrame(allNews)

    allNews.columns = ['url','image','tokenized']

    allNews['title'] = allTitles

    allNews.to_json('../data/techcrunch.json', orient="records")

    print('successfully retrieved new TechCrunch news')