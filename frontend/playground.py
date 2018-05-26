from json import dumps, loads
from Authentication import *

apikey = "2b4fec28-43af-44cf-81a1-b9d8ac02f28f"
AuthClient = Authentication(apikey)
tgt = AuthClient.gettgt()

# input_terms = ["low BP", "low blood pressure", "low cardiac output"]
input_terms = ["palpitation", "increased heart rate", "racing heat beat"]
# input_terms = ["febrile", "high temperature"]
# input_terms = ["loose stool", "frequent loose stool", "watery stool"]
# input_terms = ["Intact", "redness skin", "erythema skin"]

term_counter = {}
whole_term_list = []


def search_by_term(term, ticket):
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
    search_result_list = [j['name'] for j in jsonData]

    try:
        return search_result_list, jsonData[0]['uri']
    except:
        return search_result_list, "None"


def get_atom_list(uri, ticket):
    try:
        r = requests.get(
            uri + "/atoms", params={
                'ticket': ticket,
                'pageSize': 5000,
                'sabs': 'NANDA-I'
            }
        )
        r.encoding = 'utf-8'
        items = loads(r.text)
        # get the one want ot see
        jsonData = items["result"]
        atomlist = [j['name'] for j in jsonData]
        return atomlist
    except:
        return []


def get_relation_list(uri, ticket):
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
        relationlist = [j['relatedIdName'] for j in jsonData if j['rootSource'] == 'NANDA-I']

        return relationlist
    except:
        return []


for term in input_terms:
    ticket = AuthClient.getst(tgt)
    temp_termlist, high_possible_term_uri = search_by_term(term, ticket)
    whole_term_list += temp_termlist

    ticket = AuthClient.getst(tgt)
    temp_termlist = get_atom_list(high_possible_term_uri, ticket)
    whole_term_list += temp_termlist

    ticket = AuthClient.getst(tgt)
    temp_termlist = get_relation_list(high_possible_term_uri, ticket)
    whole_term_list += temp_termlist

print("len of result: " + str(len(whole_term_list)))
print(whole_term_list)

for term in whole_term_list:
    if term in term_counter:
        term_counter[term] += 1
    else:
        term_counter[term] = 0

print(term_counter)
print(max(term_counter, key=term_counter.get))
