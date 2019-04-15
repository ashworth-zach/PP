from flask import Flask, request
from json import dumps
from tinydb import TinyDB, Query
import os
import subprocess
from threading import Thread
import datetime
import pytz
app = Flask(__name__)
TZDB = TinyDB('TZDB.json')
Q = Query()
TZDB.upsert({'LastCompletedConcept':'Never','CONTENTID':'01'},Q.CONTENTID == '01')
TZDB.upsert({'LastCompletedKith':'Never','CONTENTID':'02'},Q.CONTENTID == '02')
TZDB.upsert({'LastCompletedUndefeated':'Never','CONTENTID':'03'},Q.CONTENTID == '03')
@app.route('/GetTZ')
def TZShow():
    return dumps(TZDB.all())
@app.route('/Shoes/<db>')
def DbShoesDefault(db):
    db = TinyDB('DBFiles/'+str(db)+'.json')
    Q = Query()
    NameList = db.search(Q.catagory == "Shoes")
    return dumps(NameList)
@app.route('/Other/<db>')
def DbShoesOtherDefault(db):
    db = TinyDB('DBFiles/'+str(db)+'.json')
    Q = Query()
    NameList = db.search(Q.catagory != "Shoes")
    return dumps(NameList)
@app.route('/Shoes/<db>/<search>')
def DbShoeSearch(db, search):
    db = TinyDB('DBFiles/'+str(db)+'.json')
    Q = Query()
    test_contains = lambda value, search: search.lower() in value.lower()
    NameList = db.search((Q.catagory == "Shoes") & (Q.title.test(test_contains, search)))
    return dumps(NameList)
@app.route('/Other/<db>/<search>')
def DbOtherSearch(db, search):
    db = TinyDB('DBFiles/'+str(db)+'.json')
    Q = Query()
    test_contains = lambda value, search: search.lower() in value.lower()
    NameList = db.search((Q.catagory != "Shoes") & (Q.title.test(test_contains, search)))
    return dumps(NameList)
@app.route('/Start/Concept')
def StartConcept():
    dir_path = os.path.dirname(os.path.realpath("./ConceptsSpider.py"))
    def MasterThreader():
        subprocess.call(["python", str(dir_path)+"/ConceptsSpider.py"])
        LastCompletedConcept = str(datetime.datetime.now(tz=pytz.timezone('US/Central')).strftime("%Y-%m-%d %H:%M")+" CST")
        TZDB.upsert({'LastCompletedConcept':LastCompletedConcept,'CONTENTID':'01'},Q.CONTENTID == '01')
    thread = Thread(target=MasterThreader)
    thread.start()
    return dumps({'completed':True})
@app.route('/Start/Kith')
def StartKith():
    dir_path = os.path.dirname(os.path.realpath("./KithScraper.py"))
    def MasterThreader():
        subprocess.call(["python", str(dir_path)+"/KithScraper.py"])
        LastCompletedKith = str(datetime.datetime.now(tz=pytz.timezone('US/Central')).strftime("%Y-%m-%d %H:%M")+" CST")
        TZDB.upsert({'LastCompletedKith':LastCompletedKith,'CONTENTID':'02'},Q.CONTENTID == '02')
    thread = Thread(target=MasterThreader)
    thread.start()
    return dumps({'started':True})
@app.route('/Start/Undefeated')
def StartUndefeated():
    dir_path = os.path.dirname(os.path.realpath("./UndefeatedSpider.py"))
    def MasterThreader():
        subprocess.call(["python", str(dir_path)+"/UndefeatedSpider.py"])
        LastCompletedUndefeated = str(datetime.datetime.now(tz=pytz.timezone('US/Central')).strftime("%Y-%m-%d %H:%M")+" CST")
        TZDB.upsert({'LastCompletedUndefeated':LastCompletedUndefeated,'CONTENTID':'03'},Q.CONTENTID == '03')
    thread = Thread(target=MasterThreader)
    thread.start()
    return dumps({'completed':True})
if __name__ == "__main__":
    try:
        os.makedirs("DBFiles")
    except FileExistsError:
        pass
    app.run(port='1337')