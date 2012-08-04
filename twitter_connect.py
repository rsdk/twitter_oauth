import urllib.request
import urllib.parse
import json
import time
import myoauth
#import re


OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
OAUTH_CONSUMER_KEY=''
OAUTH_CONSUMER_SECRET=''


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

def retweeted_by_me():
    base_url ='http://api.twitter.com/1/statuses/retweeted_by_me.json'
    parameters = generate_base_data()
    #querystring = urllib.parse.quote('?include_entities=true', safe='?')
    #print(querystring)
    request = urllib.request.Request(base_url)
    signature = myoauth.oauth_sign(request.get_method(), base_url, parameters, OAUTH_CONSUMER_SECRET, OAUTH_TOKEN_SECRET)
    header_string = generate_header_string(parameters, [['oauth_signature',signature]])
    request.add_header('Authorization', header_string)
    
    print('Authinfo: '+request.get_header('Authorization'))
    print('methodinfo: '+request.get_method())
    print('urlinfo: '+request.get_full_url())
    return urllib.request.urlopen(request)
    
    
def statuses_mentions():
    base_url = 'http://api.twitter.com/1/statuses/mentions.json'
    parameters = generate_base_data()
    request = urllib.request.Request(base_url)
    signature = myoauth.oauth_sign(request.get_method(), base_url, parameters, OAUTH_CONSUMER_SECRET, OAUTH_TOKEN_SECRET)
    header_string = generate_header_string(parameters, [['oauth_signature',signature]])
    request.add_header('Authorization', header_string)
    '''request.add_header('Authorization', 'OAuth oauth_consumer_key="'+OAUTH_CONSUMER_KEY+
                       '",oauth_nonce="'+parameters[1][1]+'",oauth_signature="'+urllib.parse.quote(signature)+
                       '",oauth_signature_method="HMAC-SHA1",oauth_timestamp="'+parameters[3][1]+
                       '",oauth_token="'+OAUTH_TOKEN+'",oauth_version="1.0"')'''

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




if __name__ == '__main__':
    

    try:
        print(getJSON(retweeted_by_me()))
    except urllib.error.HTTPError as err:
        print(err)
    '''
    #print(getJSON(get_site(['233861734','379562164'])))
                        
#print(getJSON(post_statuses_filter(['233861734','379562164'],['a'])))


# # ist %23
# space ist %20
# @ ist %40

#parseJSON(getJSON(search("%40hochschuleaalen")))
'''

