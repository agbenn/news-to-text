import pandas as pd 
import requests
import numpy as np
import datetime
from cleantext import clean
from nltk.tokenize import RegexpTokenizer
import cv2 
from PIL import Image
import sys

apiKey = 'b0c9e6c690874e5387a3b1153a49da04'
topic = sys.argv[1]
selectedDate = sys.argv[2]

baseRequest = 'http://newsapi.org/v2/everything?q='
fullRequest = baseRequest + topic + '&from=' + selectedDate + '&sortBy=publishedAt&apiKey=' + apiKey

response = requests.get(fullRequest)
if response.status_code != 200:
    print('error ' + str(response.content) + ' bad request', file = sys.stderr)

response = response.json()
results = pd.json_normalize(response['articles'])

results.content = results.content.str.replace('\n', ' ')
results.content = results.content.str.replace('\r', ' ')
results.content = results.content.str.replace('&amp;', '&')
results.content = results.content.str.replace('<[\s\S]+>', '')
results.title = results.title.str.replace('\n', ' ')
results.title = results.title.str.replace('\r', ' ')
results.title = results.title.str.replace('&amp;', '&')
results.title = results.title.str.replace('<[\s\S]+>', '')


def cleanText(wordString):
    x = clean(wordString,
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
    return x

cleanTextProcessor = np.vectorize(cleanText)

results['cleaned'] = cleanTextProcessor(results.content)
results.title = cleanTextProcessor(results.title)

tokenizer = RegexpTokenizer(r'([%$&\-\+]?\b[^\s]+\b[%$&]?)')

tokenizedData = []

for each in results.cleaned:
    tokenizedData.append(tokenizer.tokenize(each))
    
results['tokenized'] = tokenizedData
results = results.loc[:,['title', 'url', 'publishedAt','source.name', 'tokenized']]

results.columns = ['title', 'url', 'publishedAt','source', 'tokenized']

results = results.head(10)

print(results.to_json(orient="records"), file = sys.stdout)

sys.stdout.flush()


