import sys
import os
import time
from datetime import datetime
import aiohttp, asyncio
import sqlite3

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
PATH_VACS_DB = os.path.join(FILE_PATH, 'STOREvacs.db')


boTToken = 'YourTgToken_BOT'
CHAT_id = 'YourTgUserId'

NamesForDbDependsExp = {'noExperience': 'Beginer',
                        'between1And3': 'Old'}

AliasForFinalMess = {'noExperience': 'БЕЗ опыта: ',
                     'between1And3': 'С опытом от 1 до 3 лет: '}
c = 0
STOREForCurrAndCompare = []
SourcePopulDBDaily = {'noExperience': [],
                      'between1And3': []}

FourValuesForFinalDB = {'Beginer_NewToday': None,
                        'Old_NewToday': None,
                        'Beginer_TOTALToday': None,
                        'Old_TOTALToday': None}
FinalMess = '📂За последние сутки на позицию PYTHON Dev было добавлено вакански:\n\n'



async def layerForhandling400(session, page=0):
    lonuchTry = await bigReqToApiHh(session, page)
    if isinstance(lonuchTry, int):
        while isinstance(lonuchTry, int):
            await asyncio.sleep(0.3)
            lonuchTry = await bigReqToApiHh(session, page)
        return lonuchTry
    else:
        return lonuchTry
    

async def bigReqToApiHh(session, page=0):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': 'Python программист', 
        'experience': exp, 
        'area': 1,
        'per_page': 100,  
        'page': page}
    async with session.get(url, params=params) as response:
        if response.status == 200:
            return await response.json() #'noExperience'  'between1And3'
        else:
            return page
 
          
async def RunAio():
    async with aiohttp.ClientSession() as session:
        responseToApi = await layerForhandling400(session)
        total_pages = responseToApi['pages']
        ITER(responseToApi['items'])
        tasks = [layerForhandling400(session, page) for page in range(1, total_pages)]
        responses = await asyncio.gather(*tasks)
        for i in responses:
            try:
                ITER(i["items"])
            except:
                continue
            
def ITER(arg):
    global c
    for i in arg:
        c += 1
        if mode == 'SETup':
            addToDb(i["id"])
        else:
            STOREForCurrAndCompare.append(i["id"])
            

def addToDb(arg):
    pre = NamesForDbDependsExp[exp]
    with sqlite3.connect(PATH_VACS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(F"INSERT INTO {pre}TableSTOREvacs ({pre}NumsVacs) VALUES (?)", (arg,))
    

def ClearDb():
    with sqlite3.connect(PATH_VACS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM BeginerTableSTOREvacs''')
        cursor.execute('''DELETE FROM OldTableSTOREvacs''')

def ShowAllOldVacs():
    pre = NamesForDbDependsExp[exp]
    with sqlite3.connect(PATH_VACS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(F"SELECT {pre}NumsVacs FROM {pre}TableSTOREvacs")
        res = [elem[0] for elem in cursor.fetchall()]
        return res


def FormMessageTgAndUpdDb():
    global FinalMess
    OldVacs = ShowAllOldVacs()
    newVacs = set(STOREForCurrAndCompare) - set(OldVacs)
    FinalMess += F'*{AliasForFinalMess[exp]}*_{len(newVacs)} (Всего  - {len(STOREForCurrAndCompare)})_\n'

    FourValuesForFinalDB[NamesForDbDependsExp[exp] + '_NewToday'] = len(newVacs)
    FourValuesForFinalDB[NamesForDbDependsExp[exp] + '_TOTALToday'] = len(STOREForCurrAndCompare)
    
    SourcePopulDBDaily[exp] = STOREForCurrAndCompare.copy()
    STOREForCurrAndCompare.clear()
    if exp == 'between1And3':
        asyncio.get_event_loop().run_until_complete(SendToTg(FinalMess))
        # asyncio.run(SendToTg(FinalMess))
        ClearDb() 
        time.sleep(0.5)
        NewValuesInDB()
    

async def SendToTg(T):
    url = f'https://api.telegram.org/bot{boTToken}/sendMessage'
    message_params = {'chat_id': CHAT_id,
                      'text': T,
                      'parse_mode': 'Markdown'}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=message_params) as response:
            response_text = await response.text()


def NewValuesInDB():
    for v in SourcePopulDBDaily:
        PUTNewVacsInDb(v, SourcePopulDBDaily[v])

def PUTNewVacsInDb(key, Source4PopulDB):
    with sqlite3.connect(PATH_VACS_DB) as conn:
        cursor = conn.cursor()
        for num in Source4PopulDB:
            cursor.execute(F"INSERT INTO {NamesForDbDependsExp[key]}TableSTOREvacs ({NamesForDbDependsExp[key]}NumsVacs) VALUES (?)", (num,)) 


def FinishAndPopulFinalDb():
    Today = datetime.now().strftime('%d.%m.%Y')
    with sqlite3.connect(os.path.join(FILE_PATH,'FiveValuesInFinalDb.db')) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO DailyValuesFromHhApi (DATE, BeginerNewToday, OldNewToday, BeginerTOTALToday, OldTOTALToday) VALUES (?, ?, ?, ?, ?)",
                  (Today, FourValuesForFinalDB['Beginer_NewToday'], FourValuesForFinalDB['Old_NewToday'],
                  FourValuesForFinalDB['Beginer_TOTALToday'], FourValuesForFinalDB['Old_TOTALToday']))
        
    

if __name__ == '__main__':
    mode = None
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    if mode == 'daily' or mode == 'SETup':
        if mode == 'SETup':
            ClearDb()
        for exp in NamesForDbDependsExp:
            # asyncio.run(RunAio())
            asyncio.get_event_loop().run_until_complete(RunAio())
            if mode == 'daily':
                FormMessageTgAndUpdDb()
        if mode == 'daily':
            FinishAndPopulFinalDb()
                
