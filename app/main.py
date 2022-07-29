from typing import Union

from fastapi import FastAPI
import sqlite3 
import controller as controller
from shema import all_json

app = FastAPI()

@app.post("/")
async def rss(item: all_json):
    id_n = str(item).find("id=")
    id_end = str(item).find(", ")
    id = str(item)[id_n+3 : id_end]
    
    limit_n = str(item).find("limit_news=")
    limit = str(item)[limit_n+11:]

    try:
        conn = sqlite3.connect("H:\Work\Skillsoft\TZ\TZ\RSS.db")
        cursor = conn.cursor()
        cursor.execute('DELETE FROM url_rss')
        conn.commit()
        cursor.execute('INSERT OR IGNORE INTO "url_rss" ("limit_item") VALUES (?)', (int(limit), ))
        conn.commit()
    except sqlite3.Error as error:
        print('Error', error)
    finally:
        if(conn):
            conn.close()


    if int(id) == 1:
        return controller.onliner()
    elif int(id) == 2:
        return controller.drom()
    elif int(id) == 3:
        return controller.lenta()
    elif int(id) == 4:
        return controller.devby()
    elif int(id) == 5:
        return controller.s13()
    elif int(id) == 6:
        return controller.spiegel()
    elif int(id) == 7:
        return controller.krone()
    elif int(id) == 8:
        return controller.android()
    elif int(id) == 9:
        return controller.apple()
    elif int(id) == 10:
        return controller.bbc()
    elif int(id) == 11:
        return controller.komersant()#
    elif int(id) == 12:
        return controller.gazeta()#

    