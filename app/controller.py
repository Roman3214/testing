import sqlite3 
import requests
from bs4 import BeautifulSoup
import feedparser

def onliner():
    url = 'https://www.onliner.by/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('a', class_='icon-rss')

    for quote in quotes:
        try:
            conn = sqlite3.connect("RSS.db")
            cursor = conn.cursor()

            # очищаем таблицу

            cursor.execute('DELETE FROM onliner ')
            conn.commit()
            
            cursor.execute('INSERT OR IGNORE INTO "url_rss" ("url_news") VALUES (?)', (str(quote['href']),))
            conn.commit()
                
        except sqlite3.Error as error:
            print('Error', error)
        finally:
            if(conn):
                conn.close()
        try:
            conn = sqlite3.connect("RSS.db")
            cursor = conn.cursor()
            
            parse_rss_db = cursor.execute('SELECT url_news FROM url_rss ')            
            rss_urls = [i[0] for i in parse_rss_db]
            conn.commit()
                        
        except sqlite3.Error as error:
            print('Error', error)
        finally:
            if(conn):
                conn.close()

    # избавляемся от пустых значений списка          
    #   
    rs = []
    for i in rss_urls:
        if bool(i):
            rs.append(i) 

    feeds = [feedparser.parse(url)['entries'] for url in rs]
    feed = [item for feed in feeds for item in feed]

    # разбиваем по значениям данные и ложим в БД

    try:
        conn = sqlite3.connect("RSS.db")
        cursor = conn.cursor()

        for item in range(0, len(feed)):                   
            cursor.execute('INSERT OR IGNORE INTO "onliner" ("title", "all_link_news", "data_publ", "author") VALUES (?, ?, ?, ?)', (str(feed[item]['title']), str(feed[item]['link']), str(feed[item]['published']), str(feed[item]['author']), ))
            conn.commit()
        

        # устанавливаем лимит новостей

        limit_item_db = cursor.execute('SELECT limit_item FROM url_rss')
        limit_item = [i[0] for i in limit_item_db]
        conn.commit()
        
        li = []
        for i in limit_item:
            if bool(i):
                li.append(i) 

        sql = 'SELECT title, all_link_news, data_publ, author FROM onliner LIMIT'
        rss_news_db = cursor.execute(f"{sql} {str(li[0])}")
        my_list = [i for i in rss_news_db]
        
        conn.commit()
            
    except sqlite3.Error as error:
        print('Error', error)
    finally:
        if(conn):
            conn.close()    
    return my_list


def drom():

    intem_page = 1
    
    for pg in range(1, 4):
        quote_page = f'http://news.drom.ru//page{pg}.html'
        intem_page +=1
        response = requests.get(quote_page)
        soup = BeautifulSoup(response.text, 'lxml')    

        quotes = soup.find_all('a', class_='b-info-block__cont b-info-block__cont_state_reviews')

        linknews = []

        for quote in quotes:
            linknews.append(quote['href'])
        
        quotes = soup.find_all('img', class_='b-image__image b-image b-image_type_fit b-image_fit-cover')
        quotes1 = soup.find_all('div', class_='b-info-block__text b-info-block__text_type_news-date')
        quotes2 = soup.find_all('span', class_='b-ico b-ico_type_eye-gray b-ico_margin_r-size-s b-info-block__text')
        quotes3 = soup.find_all('a', class_='b-info-block__cont b-info-block__cont_state_reviews')
        
        src_img = [ item['src'] for item in quotes]
        title = [ item['title'].strip() for item in quotes]
        data = [ item.text.strip() for item in quotes1]
        views = [ item.text.strip() for item in quotes2]
        url_news = [ item['href'] for item in quotes3]

        try:
            conn = sqlite3.connect("RSS.db")
            cursor = conn.cursor()
            # очищаем таблицу
            cursor.execute('DELETE FROM onliner ')
            conn.commit()

            for item in range(0, len(data)):                   
                cursor.execute('INSERT OR IGNORE INTO "onliner" ("title", "all_link_news", "data_publ" ) VALUES (?, ?, ?)', (str(title[item]), str(url_news[item]), str(data[item]), ))
                conn.commit()
            limit_item_db = cursor.execute('SELECT limit_item FROM url_rss')
            limit_item = [i[0] for i in limit_item_db]
            conn.commit()

            # устанавливаем лимит новостей
            
            sql = 'SELECT title, all_link_news, data_publ FROM onliner LIMIT'
            rss_news_db = cursor.execute(f"{sql} {str(limit_item[0])}")
            my_list = [i for i in rss_news_db]
            
            conn.commit()
                
        except sqlite3.Error as error:
            print('Error', error)
        finally:
            if(conn):
                conn.close()
    return my_list

def lenta():
    url = 'https://lenta.ru/rss/google-newsstand/main/'
    
    feeds = feedparser.parse(url)['entries']

    # разбиваем по значениям данные и ложим в БД

    try:
        conn = sqlite3.connect("RSS.db")
        cursor = conn.cursor()
        cursor.execute('DELETE FROM onliner ')
        conn.commit()
        
        for item in range(0, len(feeds)):        
            
            cursor.execute('INSERT OR IGNORE INTO "onliner" ("title", "all_link_news", "data_publ", "author") VALUES (?, ?, ?, ?)', (str(feeds[item]['title']), str(feeds[item]['link']), str(feeds[item]['published']), str(feeds[item]['author']), ))
            conn.commit()

        
        limit_item_db = cursor.execute('SELECT limit_item FROM url_rss')
        limit_item = [i[0] for i in limit_item_db]
        conn.commit()

        # устанавливаем лимит новостей
        
        sql = 'SELECT title, all_link_news, data_publ, author FROM onliner LIMIT'
        rss_news_db = cursor.execute(f"{sql} {str(limit_item[0])}")
        my_list = [i for i in rss_news_db]
        
        conn.commit()
            
    except sqlite3.Error as error:
        print('Error', error)
    finally:
        if(conn):
            conn.close()
            #rss_str = str(my_list).replace('None', '').replace("', '", "\n").replace('), (', "\n\n").replace('[', "").replace(']', "").replace('(', "").replace(')', "").replace(', , ,', "").replace("'", "")
    
    return my_list


def devby():
    url = 'https://devby.io/rss'

    feeds = feedparser.parse(url)['entries']

    # разбиваем по значениям данные и ложим в БД

    try:
        conn = sqlite3.connect("RSS.db")
        cursor = conn.cursor()
        cursor.execute('DELETE FROM onliner ')
        conn.commit()

        for item in range(0, len(feeds)):        
            #print(feed[item]['title'])    

            # разобраться с сохраненияем ( в место ленты в бд летит онлайнер)   
            #     
            cursor.execute('INSERT OR IGNORE INTO "onliner" ("title", "all_link_news", "data_publ", "author") VALUES (?, ?, ?, ?)', (str(feeds[item]['title']), str(feeds[item]['link']), str(feeds[item]['published']), str(feeds[item]['author']), ))
            conn.commit()

        
        limit_item_db = cursor.execute('SELECT limit_item FROM url_rss')
        limit_item = [i[0] for i in limit_item_db]
        conn.commit()

        # устанавливаем лимит новостей
        
        sql = 'SELECT title, all_link_news, data_publ, author FROM onliner LIMIT'
        rss_news_db = cursor.execute(f"{sql} {str(limit_item[0])}")
        my_list = [i for i in rss_news_db]
        
        conn.commit()
            
    except sqlite3.Error as error:
        print('Error', error)
    finally:
        if(conn):
            conn.close()
            #rss_str = str(my_list).replace('None', '').replace("', '", "\n").replace('), (', "\n\n").replace('[', "").replace(']', "").replace('(', "").replace(')', "").replace(', , ,', "").replace("'", "")
    
    return my_list


def s13():
    url = 'https://s13.ru/rss/'

    feeds = feedparser.parse(url)['entries']

    # разбиваем по значениям данные и ложим в БД

    try:
        conn = sqlite3.connect("RSS.db")
        cursor = conn.cursor()

        # очищаем таблицу

        cursor.execute('DELETE FROM onliner ')
        conn.commit()

        for item in range(0, len(feeds)):    

            #добавляем в бд news
            cursor.execute('INSERT OR IGNORE INTO "onliner" ("title", "all_link_news", "data_publ") VALUES (?, ?, ?)', (str(feeds[item]['title']), str(feeds[item]['link']), str(feeds[item]['published']) ))
            conn.commit()

        # достаем лимит новостей

        limit_item_db = cursor.execute('SELECT limit_item FROM url_rss')
        limit_item = [i[0] for i in limit_item_db]
        conn.commit()

        
        
        sql = 'SELECT title, all_link_news, data_publ FROM onliner LIMIT'
        rss_news_db = cursor.execute(f"{sql} {str(limit_item[0])}")
        my_list_s13 = [i for i in rss_news_db]
      
        
        conn.commit()
            
    except sqlite3.Error as error:
        print('Error', error)
    finally:
        if(conn):
            conn.close()
            
    return my_list_s13



def spiegel():
    rss_urls = ['https://www.spiegel.de/schlagzeilen/index.rss', 'https://www.spiegel.de/schlagzeilen/index.rss']
    
    feeds = [feedparser.parse(url)['entries']for url in rss_urls]
    feed = [item for feed in feeds for item in feed]
    # разбиваем по значениям данные и ложим в БД

    try:
        conn = sqlite3.connect("RSS.db")
        cursor = conn.cursor()

        cursor.execute('DELETE FROM onliner ')
        conn.commit()
        cursor.execute('DELETE FROM url_rss WHERE url_news ')
        conn.commit()
        
        for item in range(0, len(feed)): 

            # разобраться с сохраненияем ( в место ленты в бд летит онлайнер)   
            #     
            cursor.execute('INSERT OR IGNORE INTO "onliner" ("title", "all_link_news", "data_publ") VALUES (?, ?, ?)', (str(feed[item]['title']), str(feed[item]['link']), str(feed[item]['published']), ))
            conn.commit()

        
        limit_item_db = cursor.execute('SELECT limit_item FROM url_rss')
        limit_item = [i[0] for i in limit_item_db]
        conn.commit()

        # устанавливаем лимит новостей
        
        sql = 'SELECT title, all_link_news, data_publ, author FROM onliner LIMIT'
        rss_news_db = cursor.execute(f"{sql} {str(limit_item[0])}")
        my_list = [i for i in rss_news_db]
        
        conn.commit()
            
    except sqlite3.Error as error:
        print('Error', error)
    finally:
        if(conn):
            conn.close()
    return my_list


def krone():
    url = 'https://api.krone.at/v1/rss/rssfeed-google.xml'

    feeds = feedparser.parse(url)['entries']

    # разбиваем по значениям данные и ложим в БД

    try:
        conn = sqlite3.connect("RSS.db")
        cursor = conn.cursor()

        # очищаем таблицу

        cursor.execute('DELETE FROM onliner ')
        conn.commit()

        for item in range(0, len(feeds)):    

            #добавляем в бд news
            
            cursor.execute('INSERT OR IGNORE INTO "onliner" ("title", "all_link_news", "data_publ") VALUES (?, ?, ?)', (str(feeds[item]['title']), str(feeds[item]['link']), str(feeds[item]['published']) ))
            conn.commit()

        # достаем лимит новостей

        limit_item_db = cursor.execute('SELECT limit_item FROM url_rss')
        limit_item = [i[0] for i in limit_item_db]
        conn.commit()

        
        
        sql = 'SELECT title, all_link_news, data_publ, author FROM onliner LIMIT'
        rss_news_db = cursor.execute(f"{sql} {str(limit_item[0])}")
        my_list = [i for i in rss_news_db]
      
        
        conn.commit()
            
    except sqlite3.Error as error:
        print('Error', error)
    finally:
        if(conn):
            conn.close()
            
    return my_list

    def android():
        url = 'https://androidinsider.ru/feed' 

    feeds = feedparser.parse(url)['entries']

    # разбиваем по значениям данные и ложим в БД

    try:
        conn = sqlite3.connect("RSS.db")
        cursor = conn.cursor()

        # очищаем таблицу

        cursor.execute('DELETE FROM onliner ')
        conn.commit()

        for item in range(0, len(feeds)):    

            #добавляем в бд news
            
            cursor.execute('INSERT OR IGNORE INTO "onliner" ("title", "all_link_news", "data_publ", "author") VALUES (?, ?, ?, ?)', (str(feeds[item]['title']), str(feeds[item]['link']), str(feeds[item]['published']), str(feeds[item]['author']), ))
            conn.commit()

        # достаем лимит новостей

        limit_item_db = cursor.execute('SELECT limit_item FROM url_rss')
        limit_item = [i[0] for i in limit_item_db]
        conn.commit()

        
        
        sql = 'SELECT title, all_link_news, data_publ, author FROM onliner LIMIT'
        rss_news_db = cursor.execute(f"{sql} {str(limit_item[0])}")
        my_list = [i for i in rss_news_db]
        
        
        conn.commit()
            
    except sqlite3.Error as error:
        print('Error', error)
    finally:
        if(conn):
            conn.close()
            
    return my_list


def apple():
    url = 'https://appleinsider.ru/feed' #

    feeds = feedparser.parse(url)['entries']

    # разбиваем по значениям данные и ложим в БД

    try:
        conn = sqlite3.connect("RSS.db")
        cursor = conn.cursor()

        # очищаем таблицу

        cursor.execute('DELETE FROM onliner ')
        conn.commit()

        for item in range(0, len(feeds)):    

            #добавляем в бд news
            
            cursor.execute('INSERT OR IGNORE INTO "onliner" ("title", "all_link_news", "data_publ", "author") VALUES (?, ?, ?, ?)', (str(feeds[item]['title']), str(feeds[item]['link']), str(feeds[item]['published']), str(feeds[item]['author']), ))
            conn.commit()

        # достаем лимит новостей

        limit_item_db = cursor.execute('SELECT limit_item FROM url_rss')
        limit_item = [i[0] for i in limit_item_db]
        conn.commit()

        
        
        sql = 'SELECT title, all_link_news, data_publ, author FROM onliner LIMIT'
        rss_news_db = cursor.execute(f"{sql} {str(limit_item[0])}")
        my_list = [i for i in rss_news_db]
        
        
        conn.commit()
            
    except sqlite3.Error as error:
        print('Error', error)
    finally:
        if(conn):
            conn.close()
            
    return my_list


def bbc():
    url = 'https://www.bbc.com/news'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')    

    link_news = soup.find_all('a', class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor')

    linknews = []
    for quote in link_news:
        linknews.append(f"https://www.bbc.com/{quote['href']}")

    titles = soup.find_all('h3', class_='gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text')#
    #dati = soup.find_all('time', class_='gs-o-bullet__text date qa-status-date gs-u-align-middle gs-u-display-inline')

    title = [ item.text for item in titles]
    #data = [ item['datetime'] for item in dati]

    try:
        conn = sqlite3.connect("RSS.db")
        cursor = conn.cursor()

        # очищаем таблицу

        cursor.execute('DELETE FROM onliner ')
        conn.commit()
        uy= 1
        for item in range(0, len(linknews)):  
            uy+=1
            print(uy)
            cursor.execute('INSERT OR IGNORE INTO "onliner" ("title", "all_link_news" ) VALUES (?, ?)', (str(title[item]), str(linknews[item]), ))
            conn.commit()
        limit_item_db = cursor.execute('SELECT limit_item FROM url_rss')
        limit_item = [i[0] for i in limit_item_db]
        conn.commit()

        # устанавливаем лимит новостей
        
        sql = 'SELECT title, all_link_news FROM onliner LIMIT'
        rss_news_db = cursor.execute(f"{sql} {str(limit_item[0])}")
        my_list = [i for i in rss_news_db]
        
        conn.commit()
            
    except sqlite3.Error as error:
        print('Error', error)
    finally:
        if(conn):
            conn.close()

    return my_list



def komersant():
    for pg in range(1, 3):
        
        url = ['https://tns-counter.ru/e/ec01&cid=kommersant_ru&typ=1&tms=kommersant_ru&idc=155&uid=w84a69xz0mexlroy&hid=&ver=0&type=0', f'https://www.kommersant.ru/lenta?from=all_lenta&page={pg}']
       
        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}
      
        requests.get(url[0], headers=headers)
        response = requests.post(url[1], headers=headers)
        soup = BeautifulSoup(response.text, "lxml")    
       
        link_news = soup.find_all('a', class_='uho__link uho__link--overlay')

        linknews = [ item['href'] for item in link_news]

        titles = soup.find_all('div', class_='b_ear-title')#
        dati = soup.find_all('p', class_='uho__tag rubric_lenta__item_tag hide_desktop')
        
        title = [ item.text for item in link_news]
        data = [ item.text.strip() for item in dati]
        #print(data, title, linknews)

        try:
            conn = sqlite3.connect("RSS.db")
            cursor = conn.cursor()
            # очищаем таблицу
            cursor.execute('DELETE FROM onliner ')
            conn.commit()
            if pg ==1:
                for item in range(0, len(linknews)):  
                    cursor.execute('INSERT OR IGNORE INTO "onliner" ("title", "all_link_news", "data_publ" ) VALUES (?, ?, ?)', (str(title[item]), str(linknews[item]), str(data[item]) ))
                    conn.commit()
            else:
                for item in range(0, len(linknews)):  
                    cursor.execute('INSERT OR IGNORE INTO "onliner" ("title", "all_link_news", "data_publ" ) VALUES (?, ?, ?)', (str(title[item]), str(linknews[item]), str(data[item]) ))
                    conn.commit()
        
        except sqlite3.Error as error:
                print('Error', error)
        finally:
            if(conn):
                conn.close()  
        
        try:
            conn = sqlite3.connect("RSS.db")
            cursor = conn.cursor()
            limit_item_db = cursor.execute('SELECT limit_item FROM url_rss')
            limit_item = [i[0] for i in limit_item_db]
            conn.commit()

                # устанавливаем лимит новостей
                
            sql = 'SELECT title, all_link_news FROM onliner LIMIT'
            rss_news_db = cursor.execute(f"{sql} {str(limit_item[0])}")
            my_list = [i for i in rss_news_db]
            
            conn.commit()
        except sqlite3.Error as error:
                print('Error', error)
        finally:
            if(conn):
                conn.close()
    return my_list


def gazeta():
    url = 'https://smi2.ru/data/js/93295.js'#'https://www.gazeta.ru/news/'
    headers1 = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

    response = requests.get(url, headers=headers1).json()
    url = []
    title = []

    for pg in range(0, len(response.get('news'))):
        url.append(response.get('news')[pg].get('url'))
        title.append(response.get('news')[pg].get('title'))

    for item in range(0, len(url)):    
        try:
            conn = sqlite3.connect("RSS.db")
            cursor = conn.cursor()
            
            # очищаем таблицу
            
            cursor.execute('INSERT OR IGNORE INTO "onliner" ("title", "all_link_news" ) VALUES (?, ?)', (str(title[item]), str(url[item]) ))
            conn.commit()
            
        except sqlite3.Error as error:
                print('Error', error)
        finally:
            if(conn):
                conn.close()  

    try:
        conn = sqlite3.connect("RSS.db")
        cursor = conn.cursor()
        limit_item_db = cursor.execute('SELECT limit_item FROM url_rss')
        limit_item = [i[0] for i in limit_item_db]
        conn.commit()

            # устанавливаем лимит новостей
            
        sql = 'SELECT title, all_link_news FROM onliner LIMIT'
        rss_news_db = cursor.execute(f"{sql} {str(limit_item[0])}")
        my_list = [i for i in rss_news_db]
        
        conn.commit()
    except sqlite3.Error as error:
            print('Error', error)
    finally:
        if(conn):
            conn.close()    
    return my_list