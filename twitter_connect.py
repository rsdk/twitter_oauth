import urllib.request
import urllib.parse
import json
import time
import myoauth
import re


OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
OAUTH_CONSUMER_KEY=''
OAUTH_CONSUMER_SECRET=''

# https://dev.twitter.com/docs/api
base_urls = {'GET statuses/home_timeline':'http://api.twitter.com/1/statuses/home_timeline.json',
             'GET statuses/mentions':'http://api.twitter.com/1/statuses/mentions.json',
             'GET statuses/retweeted_by_me':'http://api.twitter.com/1/statuses/retweeted_by_me.json',
             'GET statuses/retweeted_to_me':'http://api.twitter.com/1/statuses/retweeted_to_me.json',
             'GET statuses/retweets_of_me':'http://api.twitter.com/1/statuses/retweets_of_me.json',
             'GET statuses/user_timeline':'http://api.twitter.com/1/statuses/user_timeline.json',
             'GET statuses/retweeted_to_user': 'http://api.twitter.com/1/statuses/retweeted_to_user.json',
             'GET statuses/retweeted_by_user':'http://api.twitter.com/1/statuses/retweeted_by_user.json'}

def generate_base_data():
    nonce = myoauth.oauth_generate_nonce()
    timestamp = str(int(time.time()))
    base_parameters = [
              ['oauth_consumer_key',OAUTH_CONSUMER_KEY],
              ['oauth_nonce',nonce],
              ['oauth_signature_method','HMAC-SHA1'],
              ['oauth_timestamp', timestamp],
              ['oauth_token',OAUTH_TOKEN],
              ['oauth_version', '1.0']
              ]
    return base_parameters

def generate_header_string(parameters, second_list):
    parameters.extend(second_list)
    header = 'OAuth '
    for i in range(len(parameters)):
        header += parameters[i][0]+'="'+urllib.parse.quote(parameters[i][1])+'"'
        if i < len(parameters)-1:
            header += ','
    return header

def add_params(params):
    param_string= '?'
    for i in range(len(params)):
        param_string += params[i][0]+'='+params[i][1]
        if i < len(params)-1:
            param_string += '&'
    return param_string

def retweeted_by_me(query=None):
    base_url ='http://api.twitter.com/1/statuses/retweeted_by_me.json'
    parameters = generate_base_data()
    query_string = ''
    if not query == None:
        query_string = add_params(query)
        parameters.extend(query)
        #print('extended parameters: '+parameters)  
    
    #querystring = urllib.parse.quote('?include_entities=true', safe='?')
    
    request = urllib.request.Request(base_url+query_string)
    signature = myoauth.oauth_sign(request.get_method(), base_url, parameters, OAUTH_CONSUMER_SECRET, OAUTH_TOKEN_SECRET)
    header_string = generate_header_string(parameters, [['oauth_signature',signature]])
    request.add_header('Authorization', header_string)
    
    return urllib.request.urlopen(request)
    

def generic_request(base_url, query=None):
    parameters = generate_base_data()
    query_string = ''
    if not query == None:
        query_string = add_params(query)
        parameters.extend(query)
    request = urllib.request.Request(base_url+query_string)
    signature = myoauth.oauth_sign(request.get_method(), base_url, parameters, OAUTH_CONSUMER_SECRET, OAUTH_TOKEN_SECRET)
    header_string = generate_header_string(parameters, [['oauth_signature',signature]])
    request.add_header('Authorization', header_string)
    
    return urllib.request.urlopen(request)
    
def statuses_mentions(query=None):
    base_url = 'http://api.twitter.com/1/statuses/mentions.json'
    parameters = generate_base_data()
    query_string = ''
    if not query == None:
        query_string = add_params(query)
        parameters.extend(query)
        
    request = urllib.request.Request(base_url+query_string)
    signature = myoauth.oauth_sign(request.get_method(), base_url, parameters, OAUTH_CONSUMER_SECRET, OAUTH_TOKEN_SECRET)
    header_string = generate_header_string(parameters, [['oauth_signature',signature]])
    request.add_header('Authorization', header_string)

    print(request.get_header('Authorization'))
    print(request.get_method())
    print(request.get_full_url())
    return urllib.request.urlopen(request)


def search(searchterm):
    request = urllib.request.Request('http://search.twitter.com/search.json?q='+searchterm+
                                     '&result_type=mixed&page=10&rpp=100')
    return urllib.request.urlopen(request)


def list_to_string(liste):
    string = ''
    for element in liste:
        if not string == "":
            string += ','
        string += element
    print(string)
    return string
    
def post_statuses_filter(user_ids, keywords, username, password):

    a = list_to_string(user_ids)
    b = list_to_string(keywords)

    request = urllib.request.Request('https://sitestream.twitter.com/2b/site.json?follow='+a+'&track='+b)
    '''request.add_header('Authorization:', 'Basic ' + credentials)
    print('Authorization: ', 'Basic ' + credentials)'''
    return urllib.request.urlopen(request) 

def getJSON(twitterAnswer):
    Data = twitterAnswer.read().decode("utf-8")
    json_tweets = json.loads(Data)
    return(json_tweets)

def parseJSON(json):
        for element in json['results']:
            print(element['from_user_name'], end='   ')
            print(element['geo'], end='    ')
            print(element['text'])
            print()

def parseJSON_retweeted_by_me(json):
        for element in json:
            #print(element)
            print(element['retweeted_status']['user']['screen_name'])
            print(element['retweeted_status']['text'])
            print()

def formatJSON(json, space=''):
    if isinstance(json, list):
        print('LISTE:: ')
        for element in json:
            print()
            formatJSON(element, space=space+'   ')
    elif isinstance(json, dict):
        print('DICTIONARY:: ')
        for key in json:
            print(space+key, end='  ')
            formatJSON(json[key], space=space+'    ')
    else:
        print('  '+str(json))

def parse_home_timeline__tags_per_person(json):
    neues_dict = dict()
    for element in json:
        hashtagliste = hashtagsfinden(element['text'])
        
        if element['user']['name'] not in neues_dict:
            neues_dict[element['user']['name']] = hashtagliste
        else:
            neues_dict[element['user']['name']] += hashtagliste
    return neues_dict

def parse_home_timeline__tags(json):
    neues_dict = dict()
    for element in json:
        hashtagliste = hashtagsfinden(element['text'])
        
        for e in hashtagliste:
            if e not in neues_dict:
                neues_dict[e] = 1
            else:
                neues_dict[e] += 1
    return neues_dict

def hashtagsfinden(text):
    pattern = r'#\w+'
    hashtagliste = re.findall(pattern,text)
    return hashtagliste

    
if __name__ == '__main__':
    
    
    tweets = getJSON(generic_request(base_urls['GET statuses/home_timeline'],[['count','200'],['include_rts','false']]))
    #formatJSON(tweets)
    persons = parse_home_timeline__tags_per_person(tweets)
    for key in persons:
        print(key, end='    ')
        for value in persons[key]:
            print(value, end='  ')
        print()
    tags = parse_home_timeline__tags(tweets)
    for key in tags:
        print(key, end=': ')
        print(tags[key])
    
    '''
    query = [['include_entities','true'],['count','5']]
    
    try:
        tweets = parseJSON_retweeted_by_me(getJSON(retweeted_by_me(query)))
    except urllib.error.HTTPError as err:
        print(err)
    '''


# # ist %23
# space ist %20
# @ ist %40

#parseJSON(getJSON(search("%40hochschuleaalen")))

