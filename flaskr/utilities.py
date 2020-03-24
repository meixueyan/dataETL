import requests
from io import StringIO
import json
import pandas as pd
import time
from pandas.io.json import json_normalize
from xml.etree import ElementTree
import datetime as dt


def get_access_time(json_data):
  for news in json_data:
    news['Access_Time'] = dt.datetime.now()
  return json_data


def getNewsKeyword(keyword):
    #get news relating to keywords and filter language is en
    url = ('http://newsapi.org/v2/top-headlines?'
    'q=%s&'
    'language=en&'
    'apiKey=7417491a101e4ec3a8219b263f028ff7'%keyword)
  
    response = requests.get(url)  
    json_data = json.loads(response.text)['articles']  
    #add access time 
    res = get_access_time(json_data)
    data = json_normalize(res)
    return data


def getSnapshot(data):
    #display full news title
    pd.set_option('display.max_colwidth', -1)
    #select information to display & rename
    df = data[['source.name','title','publishedAt','Access_Time']]
    df = df.rename(columns={'source.name':'News_Source', 'title':'Title', 'publishedAt':'Pubulished_At'})
    #clean datetime
    df['Pubulished_At'] = df['Pubulished_At'].str.slice(0, 16)
    df['Pubulished_At'] = df['Pubulished_At'].apply(lambda x: dt.datetime.strptime(x,'%Y-%m-%dT%H:%M'))
    #remove duplicates
    df = df.drop_duplicates(subset='Title')
    #sorted the latest released news
    df = df.sort_values(by='Pubulished_At', ascending=False)
    return df


def getYieldCurve():
    url = ('http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=year(NEW_DATE)%20eq%202019')
    response = requests.get(url)
    tree = ElementTree.fromstring(response.content)
    pass


def showSnapshot(df):
    #sort index to show latest 7 days trends
    res = df.sort_index(axis=0, ascending=False)
    res = res[:7]
    return res


def getGoogleTrends(keyword):
    google_explore_api_url = 'https://trends.google.com/trends/api/explore'
    google_explore_url = 'https://trends.google.com/trends/explore'
    sess_headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    sess = requests.Session()
    params = {
        'q': keyword,
        'geo': 'US'
    }
    sess.get(google_explore_url,params=params,headers=sess_headers)
    params = {
        'hl': 'en-US',
        'tz': '-60',
        'req': '{"comparisonItem":[{"keyword":"%s","geo":"US","time":"today 12-m"}],"category":0,"property":""}'%keyword,
        'tz': '-60',
    }
    r = sess.get(google_explore_api_url,params=params,headers=sess_headers)
    token = json.loads(r.text.split(')]}\'\n')[-1])['widgets'][0]['token']
    print(token)

    # passed one year
    s2=time.strftime('%Y-%m-%d')
    # print(s2)
    year_bit = int(s2[:4])
    s1 = str(year_bit-1)+s2[4:]
    # print(s1)

    google_explore_csv_url = 'https://trends.google.com/trends/api/widgetdata/multiline/csv'
    params = {
        'req': '{"time":"%s %s","resolution":"WEEK","locale":"en-US","comparisonItem":[{"geo":{"country":"US"},"complexKeywordsRestriction":{"keyword":[{"type":"BROAD","value":"%s"}]}}],"requestOptions":{"property":"","backend":"IZG","category":0}}'%(s1,s2,keyword),
        'token':token,
        'tz': -60
    }
    r = sess.get(google_explore_csv_url,params=params,headers=sess_headers)

    data = StringIO(r.text)
    df = pd.read_csv(data)
    return df

