from flask import Flask
from flask_restful import Api, Resource, reqparse
import random
import feedparser
import requests
from bs4 import BeautifulSoup
import sqlite3

def onliner():
    url = 'https://www.onliner.by/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('a', class_='icon-rss')
    
    #rss_urls = []
    for quote in quotes:
        #rss_urls.append(quote['href'])
        try:
            conn = sqlite3.connect('RSS.db')
            cursor = conn.cursor()
            
            cursor.execute('INSERT OR IGNORE INTO "onliner" ("link_rss") VALUES (?)', (str(quote['href']),))
            conn.commit()
                
        except sqlite3.Error as error:
            print('Error', error)
        finally:
            if(conn):
                conn.close()
    try:
            conn = sqlite3.connect('RSS.db')
            cursor = conn.cursor()
            
            parse_rss_db = cursor.execute('SELECT link_rss FROM onliner ')            
            rss_urls = [i[0] for i in parse_rss_db]
            print(len(rss_urls))
            conn.commit()
                
    except sqlite3.Error as error:
        print('Error', error)
    finally:
        if(conn):
            conn.close()
    feeds = [feedparser.parse(url)['entries'] for url in str(rss_urls)]

    feed = [item for feed in feeds for item in feed]

    
    try:
        conn = sqlite3.connect('RSS.db')
        cursor = conn.cursor()
        for item in range(0, len(feed)):
            print(item)
            cursor.execute('INSERT OR IGNORE INTO "onliner" ("title", "all_link_news", "data_publ", "author") VALUES (?, ?, ?, ?)', (str(feed[item]['title']), str(feed[item]['link']), str(feed[item]['published']), str(feed[item]['author']), ))
            conn.commit()
        rss_news_db = cursor.execute('SELECT * FROM onliner ')
            #global rss_news
        rss_news = [i[0] for i in rss_news_db]
        conn.commit()
            
    except sqlite3.Error as error:
        print('Error', error)
    finally:
        if(conn):
            conn.close()

    return str(rss_news)
"""def onliner():
    url = 'https://www.onliner.by/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('a', class_='icon-rss')
    
    #rss_urls = []
    for quote in quotes:
        #rss_urls.append(quote['href'])
        try:
            conn = sqlite3.connect('RSS.db')
            cursor = conn.cursor()
            
            cursor.execute('INSERT OR IGNORE INTO "onliner" ("link_rss") VALUES (?)', (str(quote['href']),))
            conn.commit()
                
        except sqlite3.Error as error:
            print('Error', error)
        finally:
            if(conn):
                conn.close()
    try:
            conn = sqlite3.connect('RSS.db')
            cursor = conn.cursor()
            
            parse_rss_db = cursor.execute('SELECT link_rss FROM onliner ')            
            rss_urls = [i[0] for i in parse_rss_db]
            print(len(rss_urls))
            conn.commit()
                
    except sqlite3.Error as error:
        print('Error', error)
    finally:
        if(conn):
            conn.close()
    feeds = [feedparser.parse(url)['entries'] for url in str(rss_urls)]

    feed = [item for feed in feeds for item in feed]

    
    try:
        conn = sqlite3.connect('RSS.db')
        cursor = conn.cursor()
        for item in range(0, len(feed)):
            #print(item)
            cursor.execute('INSERT OR IGNORE INTO "onliner" ("title", "all_link_news", "data_publ", "author") VALUES (?, ?, ?, ?)', (str(feed[item]['title']), str(feed[item]['link']), str(feed[item]['published']), str(feed[item]['author']), ))
            conn.commit()
        rss_news_db_title = cursor.execute('SELECT title FROM onliner ')
        conn.commit()
        rss_news_db_all_link_news =cursor.execute('SELECT all_link_news FROM onliner ')
        conn.commit()
        rss_news_db_data_publ = cursor.execute('SELECT  data_publ FROM onliner ')
        conn.commit()
        rss_news_db_author = cursor.execute('SELECT author FROM onliner ')
            
        rss_news_title = [i[0] for i in rss_news_db_title]
        rss_news_all_link_news = [a[0] for a in rss_news_db_all_link_news]
        rss_news_data_publ = [s[0] for s in rss_news_db_data_publ]
        rss_news_author = [d[0] for d in rss_news_db_author]
        #conn.commit()
            
    except sqlite3.Error as error:
        print('Error', error)
    finally:
        if(conn):
            conn.close()
    rss_news = [ rss_news_all_link_news, rss_news_data_publ, rss_news_author, rss_news_title ]
    return str(rss_news)#, len(feed)"""

#onliner()
#print(news)

my_list = (
    {
        "id": 1,
        "URL": "https://www.onliner.by/",
        "RSS": onliner()#.decode('utf-8')#()#str(bytes()).encode('utf-8')
    },
    {
        "id": 2,
        "text": "hello world",
        "lang": "en"
    },
    { 
        "id": 3,
        "text": "HELLO WORLD",
        "lang": "en"
    }
)

class HiResource(Resource):
    def get(self, id = 0):
        #if id == 0:
        #    return random.choice(onliner()), 200
        #for val in my_list:
        #    if(val["id"] == id):
        #        return str(val), 200
        return str(onliner())#"Warning!", 404

    '''
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        parser.add_argument("lang")
        params = parser.parse_args()
        for val in my_list:
            if(id == val["id"]):
                val ["text"] = params["text"]
                val ["lang"] = params["lang"]
                return val, 200
        val = {
            "id": id,
            "text": params["text"],
            "lang": params["lang"]
        }
        my_list.append(val)
        return val, 201
        


    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("URL")
        parser.add_argument("amount of news")
        params = parser.parse_args()
        for val in my_list:
            if(id == val["id"]):
                return f"id= {id}", 400
        val = {
            "id": id,
            "URL": params["text"],
            "lang": params["lang"]
        }
        my_list.append(val)
        return val, 201
'''
if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(HiResource, "/rss", "/rss/", "/rss/<int:id>")
    app.run(debug=True)