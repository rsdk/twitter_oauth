import random
import hmac
import base64
import hashlib
import time
#import string
import urllib.parse

def oauth_sign(http_method, url, parameters, consumer_secret, oa_token_secret=''):
    '''
    
    
    '''
    sig =oa_calc_signature(oa_create_base_string(http_method,url,oa_collect_parameters(parameters)), 
                      oa_get_signing_key(consumer_secret, oa_token_secret))
    return sig

def oauth_generate_nonce():
    '''
    Unit Test Written
        
        
    '''
    random_number = ''.join([str(random.randint(0, 9)) for _ in range(32)])
    m = hashlib.md5((str(time.time()) + str(random_number)).encode(encoding='utf_8', errors='strict'))
    return m.hexdigest()


def oa_create_base_string(http_method, url, parameter_string):
    '''
    Unit Test Written
    
    '''
    out = http_method.upper()+'&'+ urllib.parse.quote(url,safe='') + '&' + urllib.parse.quote(parameter_string,safe='')
    #print('base_string: '+out)
    return out

def oa_get_signing_key(consumer_secret, oa_token_secret=''):
    '''
    Unit Test Written
    
    '''
    signing_key = urllib.parse.quote(consumer_secret,safe='')+'&'+urllib.parse.quote(oa_token_secret,safe='')
    return signing_key
    
   
def oa_collect_parameters(parameters):
    '''
    Unit Test Written
    
    
    '''
    #print(parameters)
    for param in parameters:
        param[1] = urllib.parse.quote(param[1],safe='')
    para_sorted = sorted(parameters, key=lambda x: x[0]) ### sorting by second item
    out =''
    for element in para_sorted:
        if not out == '':
            out += '&'
        out += element[0]+'='+element[1]
    return out

def oa_calc_signature(base_string, signing_key):
    '''
    Unit Test Written
    
    '''
    b = hmac.new(bytes(signing_key,'utf-8'), 
                 msg=bytes(base_string,'utf-8'), digestmod=hashlib.sha1)
    return base64.b64encode(b.digest()).decode('utf-8')