import requests
from bs4 import BeautifulSoup
from cleantext import clean
import re
from nltk.tokenize import RegexpTokenizer
import pandas as pd
import html

def getTokenized(text):
    firstIndex = text.find('body":"')+7
    secondIndex = 0
    if "Field Level Media" in text:
        secondIndex = text.find("Field Level Media", firstIndex)
    else:
        secondIndex = text.find('","attribution"', firstIndex)
    content = text[firstIndex:secondIndex]


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
    cleanr = re.compile('<.*?>')
    content = re.sub(cleanr, '', content)
    content = content.replace('\n',' ')
    content = content.replace('\t',' ')


    tokenizer = RegexpTokenizer(r'([%$&\-\+]?\b[^\s]+\b[%$&]?)')
    content = tokenizer.tokenize(content)
    return content

def getImageURL(text):
    firstIndex = text.find('image" content="')+16
    secondIndex = text.find('/>', firstIndex)
    content = text[firstIndex:(secondIndex-2)]


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
    return content

def getReutersSports(sport):
    baseURL = ''
    filePath = '../data/'

    if sport == 'nba':
        baseURL = 'https://www.reuters.com/news/archive/basketball-nba'
        filePath = filePath + 'nba.json'
    elif sport == 'nfl':
        baseURL = 'https://www.reuters.com/news/archive/football-nfl'
        filePath = filePath + 'nfl.json'
    elif sport == 'nhl':
        baseURL = 'https://www.reuters.com/news/archive/icehockey-nhl'
        filePath = filePath + 'nhl.json'
    else:
        print('topic is not supported')
        return 'error: topic is not supported'

    response = requests.get(baseURL)
    soup = BeautifulSoup(response.text, 'html.parser')

    allAs = soup.find_all("div", class_='story-content')

    allRefs = []
    allNews = []

    for each in allAs:
        x = baseURL + each.find_all("a")[0]['href']
        allRefs.append(x)

    for each in allRefs:
        try:
            response = requests.get(each)
            text = response.text
            content = getTokenized(text)
            image = getImageURL(text)
            soup = BeautifulSoup(text, 'html.parser')
            x = soup.find_all('h1')
            title = x[0].text
            allNews.append([each,image,content,title])
        except:
            print('unable to retrieve data for article: ' + each)

    allNews = pd.DataFrame(allNews)

    allNews.columns = ['url','image','tokenized','title']

    allNews.to_json(filePath, orient="records")

    print('successfully retrieved ' + sport + ' news')

