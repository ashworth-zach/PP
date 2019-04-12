from flask import Flask, request
from json import dumps
from tinydb import TinyDB, Query
import os
import subprocess
app = Flask(__name__)

@app.route('/Shoes/<db>')
def DbShoesDefault(db):
    db = TinyDB('DBFiles'+str(db)+'.json')
    Q = Query()
    NameList = db.search(Q.catagory == "Shoes")
    return dumps(NameList)
@app.route('/Other/<db>')
def DbShoesOtherDefault(db):
    db = TinyDB('DBFiles'+str(db)+'.json')
    Q = Query()
    NameList = db.search(Q.catagory != "Shoes")
    return dumps(NameList)
@app.route('/Shoes/<db>/<search>')
def DbShoeSearch(db, search):
    db = TinyDB('DBFiles'+str(db)+'.json')
    Q = Query()
    test_contains = lambda value, search: search.lower() in value.lower()
    NameList = db.search((Q.catagory == "Shoes") & (Q.title.test(test_contains, search)))
    return dumps(NameList)
@app.route('/Other/<db>/<search>')
def DbOtherSearch(db, search):
    db = TinyDB('DBFiles'+str(db)+'.json')
    Q = Query()
    test_contains = lambda value, search: search.lower() in value.lower()
    NameList = db.search((Q.catagory != "Shoes") & (Q.title.test(test_contains, search)))
    return dumps(NameList)
@app.route('/Start/Concept')
def StartConcept():
    dir_path = os.path.dirname(os.path.realpath("./ConceptsSpider.py"))
    subprocess.call(["python", str(dir_path)+"/ConceptsSpider.py"])
    return dumps({'completed':True})
@app.route('/Start/Kith')
def StartKith():
    dir_path = os.path.dirname(os.path.realpath("./KithScraper.py"))
    subprocess.call(["python", str(dir_path)+"/KithScraper.py"])
    return dumps({'completed':True})
@app.route('/Start/Undefeated')
def StartUndefeated():
    dir_path = os.path.dirname(os.path.realpath("./UndefeatedScraper.py"))
    subprocess.call(["python", str(dir_path)+"/UndefeatedScraper.py"])
    return dumps({'completed':True})
if __name__ == "__main__":
    app.run(port='1337')