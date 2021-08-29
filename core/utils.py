import json
import requests
from rest_framework.response import Response


TORRE_ROOT_URL = "https://search.torre.co/people/_search"

TORRE_SEARCH_PERSON_URL = TORRE_ROOT_URL 

HEADERS = {'Content-Type': 'application/json'}

LANGUAGES = [
    ("ESP","Spanish"),
    ("ENG","English"),
    ("GER","German"),
    ("FRC","French"),
    ("CHI","Chinese"),
    ("ITA","Italian"),
    ("JAP","Japanese"),
    ("ARB","Arabic"),
]


def url_builder(size,lang,aggregate):
    """
        Build a simple url with the given params,
        @notice by default aggregate always False
    """
    if aggregate == False:
        query = "?size={}&lang={}&aggregate{}".format(size,lang,"false")
    return TORRE_SEARCH_PERSON_URL + query


def check_torre_user(username,size,lang):
    """
        Retrive users info and check if the same 
        username exists on torre-db, if exists
        store the torre-user-info
    """
    payload = json.dumps({
                  "name": {
                    "term": username
                  }
                })
    response =  requests.request('POST',
                            url_builder(size,lang,False),
                            headers=HEADERS,
                            data=payload)
    if(response.status_code == 200):
        data = json.loads(response.text)
        for results in data['results']:
            print(results['name'],results['username'])
            #for e in results:
            #        if e == 'name':
            #            print(results[e])
        return (True,json.loads(response.text))

    else: 
        print("Error:::", response.text)
        return (False,None)



def search_common_interests(interest,size,lang):
    """
        Search for people with the same interests 
        as the user
    """
    data = []
    data
    print("inte",interest)
    for i in interest:
        payload = json.dumps({
            "and":
                [{
                    "skill/role":{
                                "text":"django",
                                "experience":"1-plus-year"
                                }}]
        })
        response = requests.request('POST',
                                url_builder(size,lang,False),
                                headers=HEADERS,
                                data=payload)
        
        for result in json.loads(response.text)['results']:
            data.append({
                        'name':result['name'],
                        'username':result['username'],
                        'image':result['image'],
                        'skills':result['skills']
                        })
    return data




def failed_response(description):
    """
        General interface for returning
        failed requests
    """

    return Response({
        "status":False,
        "description":description
    })


def accepted_response(data=False):
    """
        General interface for returning
        failed requests
    """
    if (bool(data)):
        return Response({
            "status":True,
            "data":data
        })
    else:
        return Response({"status":True})

