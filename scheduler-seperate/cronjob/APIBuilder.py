import requests
import json
import Utility as util

# print api result
def print_result(response):
    print("---------returns----------")
    print(response.status_code)
    print(response.text)

# api request caller
def api_resp_check(response, endpoint):
    print("API call: "+endpoint)
    if response.status_code != 200:
        print("----------ERROR-------------")
        print_result(response)
        util.script_exit(False)

def controlHubLogin(user,pswd, config):
    headers = {
        'Content-Type': 'application/json',
        'X-Requested-By': 'SDC',
    }
    data = '{"userName":"'+user+'", "password":"'+pswd+'"}'
    response = requests.post(url=config['URL']['CONTROL_HUB_AUTH'], headers=headers, data=data)
    return response

def getSessionToken(user,pswd, config):
    response = controlHubLogin(user,pswd,config)
    if (response.status_code != 200):
        return ""    
    cookies = response.cookies
    return cookies.items()[0][1]

def setAuthToken(user,pswd, config):
    _sessionToken = getSessionToken(user,pswd,config)
    if _sessionToken == "":
        return False
    util.writeToFile("token.txt",_sessionToken)
    return True


# get header for data collector api
def get_api_headers():
    _sessionToken = util.readFile("token.txt")
    print("token: "+_sessionToken)
    return {
            'Content-Type': 'application/json',
            'X-Requested-By': 'SDC',
            'X-SS-REST-CALL': 'true',
            'X-SS-User-Auth-Token': _sessionToken
        }

def sch_api_get_request(config, endpoint, params=None, data=None):

    if data and params:
        response = requests.get(config['URL']['HOST']+endpoint, headers=get_api_headers(), params=params, json=data)
    elif data:
        response = requests.get(config['URL']['HOST']+endpoint, headers=get_api_headers(), json=data)
    elif params:
        response = requests.get(config['URL']['HOST']+endpoint, headers=get_api_headers(), params=params)
    else:
        response = requests.get(config['URL']['HOST']+endpoint, headers=get_api_headers())
    api_resp_check(response, endpoint)
    return response

def sch_api_post_request(config, endpoint, params=None, data=None):

    if data and params:
        response = requests.post(config['URL']['HOST']+endpoint, headers=get_api_headers(), params=params, json=data)
    elif data:
        response = requests.post(config['URL']['HOST']+endpoint, headers=get_api_headers(), json=data)
    elif params:
        response = requests.post(config['URL']['HOST']+endpoint, headers=get_api_headers(), params=params)
    else:
        response = requests.post(config['URL']['HOST']+endpoint, headers=get_api_headers())
    api_resp_check(response, endpoint)
    return response

def sch_api_put_request(config, endpoint, data=None):
    response = requests.put(config['URL']['HOST']+endpoint, headers=get_api_headers(), json=data)
    api_resp_check(response, endpoint)
    return response

