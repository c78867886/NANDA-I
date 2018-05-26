from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api, reqparse
from flask_jsonpify import jsonify
from pymongo import MongoClient
from json import dumps, loads
import datetime
from Searchterms import *
from nltk.corpus import brown
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_token_from_uts():
    post_r = requests.post(
        "https://umls.terminology.tools/security/authenticate/c78867886",
        headers={
            "Content-Type": "text/plain",
            "Accept": "application/xml"
        },
        data="Mars-0504"
    )
    post_r.encoding = 'utf-8'
    soup = BeautifulSoup(post_r.text, "lxml")
    return soup.find_all("authtoken")[0].get_text()

#brownword = list(set([i.lower() for i in brown.words()]))
# sorted(brownword)


# Connect MongoDB
connection = MongoClient('ds253879.mlab.com', 53879)
dbname = 'practice'
db = connection[dbname]
username, password = 'usr1', '123'
db.authenticate(username, password)
keywordlist = db.keywordlist

api = Api(app)

CORS(app)


@app.route("/")
def index():
    # update keyword history
    parser = reqparse.RequestParser()
    parser.add_argument('keyworddc', type=str)
    parser.add_argument('keywordrelatedf', type=str)
    parser.add_argument('keywordriskf', type=str)
    args = parser.parse_args()
    #keyword = {'keyword': args['keyword'], 'date': datetime.datetime.now()}
    # keywordlist.insert_one(keyword)

    # get search result
    # print(args['keyword'])
    searchlist = {
        "defining_characteristic_of": [k.lstrip().rstrip() for k in args['keyworddc'].split(';')[:-1]],
        "related_factor_of": [k.lstrip().rstrip() for k in args['keywordrelatedf'].split(';')[:-1]],
        "risk_factor_of": [k.lstrip().rstrip() for k in args['keywordriskf'].split(';')[:-1]],
    }
    #searchterms = Searchterms(args['keyword'], "word")
    searchterms = Searchterms(searchlist, "word")
    searchresult = searchterms.getsearchresult()
    # print(type(searchresult))
    # return dumps(searchresult)
    return dumps(searchresult)


class Keywordhistory(Resource):
    def get(self):
        keywordhistory = keywordlist.find().sort('date', -1).limit(5)
        #print(dumps([k for k in keywordhistory], default=self.datetime_converter))

        return dumps([k for k in keywordhistory], default=self.datetime_converter)

    def datetime_converter(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()


class Getsuggestion(Resource):
    # token from UTS
    token = get_token_from_uts()

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', type=str)
        args = parser.parse_args()
        keyword = args['keyword'].split(";")[-1].lstrip().rstrip()
        #keyword = args['keyword']

        if keyword != "":
            r = requests.get(
                "https://umls.terminology.tools/content/concept/UMLS/latest/autocomplete/" + keyword,
                headers={'Authorization': self.token}
                #headers={'Authorization': '2b4fec28-43af-44cf-81a1-b9d8ac02f28f'}
            )
            if r.status_code != 200:
                self.token = get_token_from_uts()
                r = requests.get(
                    "https://umls.terminology.tools/content/concept/UMLS/latest/autocomplete/" + keyword,
                    headers={'Authorization': self.token}
                )

            r.encoding = 'utf-8'
            items = loads(r.text)
            result = sorted(items["strings"], key=len)[:10]
            print(result)
            return result


class Getfactor(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code', type=str)
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        code = args['code']
        name = args['name']

        searchterms = Searchterms()
        t = searchterms.get_factor_of_term(code, name)

        return t


api.add_resource(Keywordhistory, '/keywordhistory')  # Route_for_Keywordhistory
api.add_resource(Getsuggestion, '/suggestion')  # Route_for_Getsuggestion
api.add_resource(Getfactor, '/getfactor')  # Route_for_Getsuggestion


if __name__ == '__main__':
    app.run(port=5002)
