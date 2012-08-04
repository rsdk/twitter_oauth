import urllib.request
import urllib.parse
import json
import time
import myoauth
#import re


OAUTH_TOKEN = '317365878-TCmMFSLaLSgglxZ7mHx4htpvqfYQQLE6p2j2hZWl'
OAUTH_TOKEN_SECRET = 'ihAxyMFn3RhUqVLL1n0idtTvYk0b7lCz1kma4LWLrY'
OAUTH_CONSUMER_KEY='lOewnflbE5LpQJtcJHlyCA'
OAUTH_CONSUMER_SECRET='Qpp69d9QTJiyqLlSKhPSkmBIMbG0Y3S1d7XnR3pDk'



def tweet(username, password, message):
    encoded_msg = urllib.parse.urlencode({'status': message})
    request = urllib.request.Request(
         'http://api.twitter.com/1/statuses/update.json')
    request.add_header('Authorization: ', 'Basic ' )
    urllib.request.urlopen(request, encoded_msg)
    
def get_statuses_mentions():
    base_url ='http://api.twitter.com/1/statuses/mentions.json'
    nonce = myoauth.oauth_generate_nonce()
    timestamp = str(int(time.time()))
    request = urllib.request.Request(base_url+'?include_entities=true')
    parameters = [
              ['include_entities','true'],
              ['oauth_consumer_key',OAUTH_CONSUMER_KEY],
              ['oauth_nonce',nonce],
              ['oauth_signature_method','HMAC-SHA1'],
              ['oauth_timestamp', timestamp],
              ['oauth_token',OAUTH_TOKEN],
              ['oauth_version', '1.0']
              ]
    signature = myoauth.oauth_sign(request.get_method(), base_url, parameters, OAUTH_CONSUMER_SECRET, OAUTH_TOKEN_SECRET)
    
    request.add_header('Authorization:', 'OAuth oauth_consumer_key="'+OAUTH_CONSUMER_KEY+
                       '",oauth_nonce="'+nonce+'",oauth_signature="'+signature+
                       '",oauth_signature_method="HMAC-SHA1",oauth_timestamp="'+timestamp+
                       '",oauth_token="'+OAUTH_TOKEN+'",oauth_version="1.0"')

    print(request.get_header('Authorization:'))
    print(request.get_method())
    print(request.get_full_url())
    return urllib.request.urlopen(request)
    
    
''' OAuth 1.0a'''
def get_statuses_home_timeline():
    base_url = 'http://api.twitter.com/1/statuses/home_timeline.json'
    nonce = myoauth.oauth_generate_nonce()
    timestamp = str(int(time.time()))
    request = urllib.request.Request(base_url+'?include_entities=true')
    parameters = [
              ['include_entities','true'],
              ['oauth_consumer_key',OAUTH_CONSUMER_KEY],
              ['oauth_nonce',nonce],
              ['oauth_signature_method','HMAC-SHA1'],
              ['oauth_timestamp', timestamp],
              ['oauth_token',OAUTH_TOKEN],
              ['oauth_version', '1.0']
              ]
    signature = myoauth.oauth_sign(request.get_method(), base_url, parameters, OAUTH_CONSUMER_SECRET, OAUTH_TOKEN_SECRET)
    
    request.add_header('Authorization:', 'OAuth oauth_consumer_key="'+OAUTH_CONSUMER_KEY+
                       '",oauth_nonce="'+nonce+'",oauth_signature="'+signature+
                       '",oauth_signature_method="HMAC-SHA1",oauth_timestamp="'+timestamp+
                       '",oauth_token="'+OAUTH_TOKEN+'",oauth_version="1.0"')

    print(request.get_header('Authorization:'))
    print(request.get_method())
    print(request.get_full_url())
    return urllib.request.urlopen(request)


def search(searchterm):
    request = urllib.request.Request('http://search.twitter.com/search.json?q='+searchterm+
                                     '&result_type=mixed&page=10&rpp=100')
    return urllib.request.urlopen(request)

def get_site(user_ids):
    a = list_to_string(user_ids)
    baseurl = 'http://sitestream.twitter.com/2b/site.json'
    f = 'follow'
    nonce = myoauth.oauth_generate_nonce()
    timestamp = str(int(time.time()))
    request = urllib.request.Request('http://sitestream.twitter.com/2b/site.json?follow='+a)
    print(request.get_method())
    parameters = [
                  [f,a],
                  ['oauth_consumer_key',OAUTH_CONSUMER_KEY],
                  ['oauth_nonce',nonce],
                  ['oauth_signature_method','HMAC-SHA1'],
                  ['oauth_timestamp', timestamp],
                  ['oauth_token',OAUTH_TOKEN],
                  ['oauth_version', '1.0']
                  ]
    print(parameters)
    signature = myoauth.oauth_sign(request.get_method(),baseurl,
                     parameters,
                     OAUTH_CONSUMER_SECRET, OAUTH_TOKEN_SECRET)
    
    request.add_header('Authorization:', 'OAuth '+'oauth_consumer_key="'+OAUTH_CONSUMER_KEY+
                       '",oauth_nonce="'+nonce+'",oauth_signature="'+signature+
                       '",oauth_signature_method="HMAC-SHA1",oauth_timestamp="'+timestamp+
                       '",oauth_token="'+OAUTH_TOKEN+'",oauth_version="1.0"')

    print(request.header_items())
    print(request.get_method())
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
    '''
    out = oauth_sign('post','https://sitestream.twitter.com/2b/site.json',
                     [['oauth_consumer_key',OAUTH_CONSUMER_KEY],['oauth_nonce',oauth_generate_nonce()],
                      ['oauth_token',OAUTH_TOKEN],['oauth_version', str(1.0)],
                      ['oauth_timestamp', str(int(time.time()))],['oauth_signature_method','HMAC-SHA1']],
                     OAUTH_CONSUMER_SECRET, OAUTH_TOKEN_SECRET)
    print(out)

#print(home_timeline)
'''
    print(getJSON(get_statuses_mentions()))
    #print(getJSON(get_site(['233861734','379562164'])))
'''                           
#print(getJSON(post_statuses_filter(['233861734','379562164'],['a'])))


# # ist %23
# space ist %20
# @ ist %40

#parseJSON(getJSON(search("%40hochschuleaalen")))
'''

