from core.models import LANGUAGES
import json
import requests
from rest_framework.response import Response
from users.models import Profile

TORRE_ROOT_URL = "https://search.torre.co/people/_search"

BIOS_URL = "https://torre.bio/api/bios/"

TORRE_SEARCH_PERSON_URL = TORRE_ROOT_URL 

HEADERS = {'Content-Type': 'application/json'}

def get_profile_by_id(id):
    try:
        if type(id) == int:
            profile = Profile.objects.get(id=id)
            return profile
        else:
            return None    
    except:
        return None

def url_builder(size,lang,aggregate):
    """
        Build a simple url with the given params,
        @notice by default aggregate always False
    """
    if aggregate == False:
        query = "?size={}&lang={}&aggregate={}".format(size,lang,"true")
        print(TORRE_SEARCH_PERSON_URL + query)
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

    print(interest,size,lang)
    for i in interest:
        print(i)
        payload = json.dumps({
            "and":
                [
                {"skill/role": {"text":i,"experience":"1-plus-year"}}
                ]
        })

        response = requests.request('POST',
                                url_builder(size,lang,False),
                                headers=HEADERS,
                                data=payload)
        
        if response.status_code == 200:
            for result in json.loads(response.text)['results']:
                langs = get_meta_data(result['username'])
                data.append({
                            'username':result['username'],
                            'name':result['name'],
                            'description':result['professionalHeadline'],
                            'image':result['picture'],
                            'skills':result['skills'],
                            'langs':langs
                            })
        else:
            print("Error:::",response.content)
            return None
    return data


def get_meta_data(username):
    response = requests.request('GET',
                                BIOS_URL+username)
    data =  json.loads(response.text)
    return data['languages']


def is_lang_valid(lang):
    try:
        for l in LANGUAGES:
            if l[0].lower() == lang.lower():
                return True
        return False
    except:
        raise SyntaxError("The language given is not correct")



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

