#################################################################################
# usage of the script
# usage: python search-terms.py -k APIKEY -v VERSION -s STRING
# see https://documentation.uts.nlm.nih.gov/rest/search/index.html for full docs
# on the /search endpoint
#################################################################################

from Authentication import *
import requests
import json
import time
from json import dumps, loads

apikey = "2b4fec28-43af-44cf-81a1-b9d8ac02f28f"
version = "current"
uri = "https://uts-ws.nlm.nih.gov"
content_endpoint = "/rest/search/" + version


class Searchterms:
    def __init__(self, searchlist=[], searchtype="word"):
        # self.username=username
        # self.password=password
        self.searchlist = searchlist  # "[ 'Therapeutic', 'fever' ]"
        self.searchtype = searchtype  # "word"
        self.sabs = "NANDA-I"
        self.AuthClient = Authentication(apikey)
        self.tgt = self.AuthClient.gettgt()

    def getsearchresult(self):
        termlist = []

        for additional_label, label_term_list in self.searchlist.items():
            for dc in label_term_list:
                searchtermlist = self.search_by_term(dc, self.AuthClient)

                for w in searchtermlist[:3]:  # [ [uri, name], [uri, name], [uri, name] ]
                    atomlist = self.get_atom_list(w[0], self.AuthClient)  # (code eg. 00011)[uri, uri, uri...]
                    for a in atomlist:
                        relationlist = self.get_relation_list(a, self.AuthClient, additional_label)
                        for rl in relationlist:
                            termlist.append((rl[0], rl[1]))

        term_counter = {}
        for term in termlist:
            if term in term_counter:
                term_counter[term] += 1
            else:
                term_counter[term] = 1

        # print(term_counter)
        result = [t for t in sorted([[list(key), value] for key, value in term_counter.items() if value >= 2], key=lambda t: t[1], reverse=True)][:5]
        # print(result)
        self.get_code(result)
        result = [{'name': r[0][0], 'code':r[0][1], 'frequency':r[1]} for r in result]

        return result

    def get_code(self, result):
        for res in result:
            ticket = self.AuthClient.getst(self.tgt)
            for w in self.search_by_term(res[0][0], self.AuthClient)[:3]:
                ticket = self.AuthClient.getst(self.tgt)
                try:
                    r = requests.get(
                        w[0] + "/atoms", params={
                            'ticket': ticket,
                            'pageSize': 5000,
                            'sabs': self.sabs
                        }
                    )
                    r.encoding = 'utf-8'
                    items = loads(r.text)
                    # get the one want ot see
                    jsonData = items["result"]
                except:
                    jsonData = []
                for j in jsonData:
                    #print(j['ui'] + " " + re[0][1])
                    if j['ui'] == res[0][1]:
                        res[0][1] = j['code'].split('/')[-1]

    def search_by_term(self, term, AuthClient):
        try_times = 1
        while True:
            if try_times > 3:
                break
            try_times += 1
            try:
                ticket = AuthClient.getst(self.tgt)
                r = requests.get(
                    "https://uts-ws.nlm.nih.gov/rest/search/current", params={
                        'ticket': ticket,
                        'string': term,
                        'pageSize': 5000
                    }
                )
                r.encoding = 'utf-8'
                items = loads(r.text)
                # get the one want ot see
                jsonData = items["result"]["results"]
                search_result_list = [[j['uri'], j['name']] for j in jsonData]
            except:
                print(term)
                print("search_by_term fail")
                #print('error code: ' + str(r.status_code))
                search_result_list = []

        return search_result_list

    def get_atom_list(self, uri, AuthClient):
        try_times = 1
        while True:
            try:
                if try_times > 3:
                    return []
                try_times += 1
                ticket = AuthClient.getst(self.tgt)
                r = requests.get(
                    uri + "/atoms", params={
                        'ticket': ticket,
                        'pageSize': 5000,
                        'sabs': self.sabs
                    }
                )
                r.encoding = 'utf-8'
                # print(r.status_code)
                items = loads(r.text)
                # get the one want ot see
                jsonData = items["result"]
                atomlist = [j['code'] for j in jsonData]
                return atomlist
            except Exception as err:
                print("get_atom_list fail")
                # print('Atom list error: ' + str(err))

    def get_relation_list(self, uri, AuthClient, additional_label):
        ticket = AuthClient.getst(self.tgt)
        try:
            r = requests.get(
                uri + "/relations", params={
                    'ticket': ticket,
                    'pageSize': 5000
                }
            )
            r.encoding = 'utf-8'
            items = loads(r.text)
            # get the one want ot see
            jsonData = items["result"]
            relationlist = [[j['relatedIdName'], j['relatedId'].split('/')[-1]] for j in jsonData if j['rootSource'] == self.sabs and j['additionalRelationLabel'] == additional_label]

            return relationlist
        except:
            print("get_relation_list fail")
            print('error code: ' + str(r.status_code))
            return []

    def get_factor_of_term(self, code, name):
        defining_char_list = []
        related_factor_list = []
        risk_factor_list = []

        ticket = self.AuthClient.getst(self.tgt)
        try:
            r = requests.get(
                'https://uts-ws.nlm.nih.gov/rest/content/current/source/NANDA-I/' + code + '/relations', params={
                    'ticket': ticket,
                    'pageSize': 5000
                }
            )
            r.encoding = 'utf-8'
            print(r.status_code)
            items = loads(r.text)
            # get the one want ot see
            jsonData = items["result"]
            for j in jsonData:
                if j['additionalRelationLabel'] == 'has_defining_characteristic':
                    defining_char_list.append(j['relatedIdName'])
                elif j['additionalRelationLabel'] == 'has_related_factor':
                    related_factor_list.append(j['relatedIdName'])
                elif j['additionalRelationLabel'] == 'has_risk_factor':
                    risk_factor_list.append(j['relatedIdName'])
        except Exception as err:
            print("get_factor_list fail: " + str(err))

        return {'name': name, 'defining_char': defining_char_list, 'related_factor': related_factor_list, 'risk_factor': risk_factor_list}


if __name__ == '__main__':
    #searchterms = Searchterms(['borborygmi', 'anorexia', 'headache', 'nausea', 'vomiting', 'Constipation'], "word")
    searchlist = {
        "defining_characteristic_of": ['anorexia', 'vomiting'],
        "related_factor_of": ['Confusion', 'Dehydration'],
        "risk_factor_of": [],
    }
    #searchterms = Searchterms(['absent pulses', 'claudication', 'edema', 'smking', 'hypertension'], "word")
    searchterms = Searchterms(searchlist, 'word')
    t = searchterms.getsearchresult()
    #t = searchterms.get_factor_of_term('00011')
    print(t)

    #uri0 = searchterms.cuilist[0]
