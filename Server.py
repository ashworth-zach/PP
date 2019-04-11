from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from tinydb import TinyDB, Query
import os
import subprocess
app = Flask(__name__)
api = Api(app)

class DbShoesDefault(Resource):
    def get(self, db):
        db = TinyDB('DBFiles/'+str(db)+'.json')
        Q = Query()
        test_contains = lambda value, search: search.lower() in value.lower()
        NameList = db.search(Q.catagory == "Shoes")
        return NameList
class DbShoesOtherDefault(Resource):
    def get(self, db):
        db = TinyDB('DBFiles/'+str(db)+'.json')
        Q = Query()
        test_contains = lambda value, search: search.lower() in value.lower()
        NameList = db.search(Q.catagory != "Shoes")
        return NameList
class DbShoeSearch(Resource):
    def get(self, db, search):
        db = TinyDB('DBFiles/'+str(db)+'.json')
        Q = Query()
        test_contains = lambda value, search: search.lower() in value.lower()
        NameList = db.search((Q.catagory == "Shoes") & (Q.title.test(test_contains, search)))
        return NameList
class DbOtherSearch(Resource):
    def get(self, db, search):
        db = TinyDB('DBFiles/'+str(db)+'.json')
        Q = Query()
        test_contains = lambda value, search: search.lower() in value.lower()
        NameList = db.search((Q.catagory != "Shoes") & (Q.title.test(test_contains, search)))
        return NameList
class StartConcept(Resource):
    def get(self):
        dir_path = os.path.dirname(os.path.realpath("./ConceptsSpider.py"))
        subprocess.call(["python", str(dir_path)+"/ConceptsSpider.py"])
        return {'completed':True}
class StartKith(Resource):
    def get(self):
        dir_path = os.path.dirname(os.path.realpath("./KithScraper.py"))
        subprocess.call(["python", str(dir_path)+"/KithScraper.py"])
        return {'completed':True}
class StartUndefeated(Resource):
    def get(self):
        dir_path = os.path.dirname(os.path.realpath("./UndefeatedScraper.py"))
        subprocess.call(["python", str(dir_path)+"/UndefeatedScraper.py"])
        return {'completed':True}
api.add_resource(DbShoesDefault, '/Shoes/<db>')
api.add_resource(DbShoesOtherDefault, '/Other/<db>')
api.add_resource(DbShoeSearch, '/Shoes/<db>/<search>')
api.add_resource(DbOtherSearch, '/Other/<db>/<search>')
api.add_resource(StartConcept, '/Start/Concept')
api.add_resource(StartKith, '/Start/Kith')
api.add_resource(StartUndefeated, '/Start/Undefeated')
if __name__ == "__main__":
    app.run(port='1337')