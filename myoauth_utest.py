'''
Created on 01.08.2012

@author: rene
'''
import unittest
import myoauth
from myoauth import oa_get_signing_key, oa_calc_signature, oa_collect_parameters


class TestOAuth(unittest.TestCase):


    def test_oauth_generate_nonce(self):
        test_nonce = 'kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg'
        ''' nonce erzeugen'''
        nonce = myoauth.oauth_generate_nonce()
        '''prüfen ob 32 Zeichen nicht notwendig'''
        #self.assertEqual(len(nonce), len(test_nonce))
        '''prüfen ob nur erlaubte Zeichen'''
        self.assertTrue(nonce.isalnum())
        
    def test_oa_generate_base_string(self):
        test_parameter_string = 'include_entities=true&oauth_consumer_key=xvz1evFS4wEEPTGEFPHBog&oauth_nonce=kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg&oauth_signature_method=HMAC-SHA1&oauth_timestamp=1318622958&oauth_token=370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb&oauth_version=1.0&status=Hello%20Ladies%20%2B%20Gentlemen%2C%20a%20signed%20OAuth%20request%21'
        test_sig_base_string = 'POST&https%3A%2F%2Fapi.twitter.com%2F1%2Fstatuses%2Fupdate.json&include_entities%3Dtrue%26oauth_consumer_key%3Dxvz1evFS4wEEPTGEFPHBog%26oauth_nonce%3DkYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1318622958%26oauth_token%3D370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb%26oauth_version%3D1.0%26status%3DHello%2520Ladies%2520%252B%2520Gentlemen%252C%2520a%2520signed%2520OAuth%2520request%2521'
        generated_sig_base_string = myoauth.oa_create_base_string('POST', 'https://api.twitter.com/1/statuses/update.json', test_parameter_string)
        self.assertEqual( test_sig_base_string  , generated_sig_base_string)
        
    def test_oa_get_signing_key(self):
        test_consumer_secret = 'kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw'
        test_oauth_token_secret = 'LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE'
        test_signing_key = 'kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw&LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE'
        self.assertEqual( oa_get_signing_key(test_consumer_secret, test_oauth_token_secret ), test_signing_key)
        
    def test_calc_signature(self):
        test_sig_base_string = 'POST&https%3A%2F%2Fapi.twitter.com%2F1%2Fstatuses%2Fupdate.json&include_entities%3Dtrue%26oauth_consumer_key%3Dxvz1evFS4wEEPTGEFPHBog%26oauth_nonce%3DkYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1318622958%26oauth_token%3D370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb%26oauth_version%3D1.0%26status%3DHello%2520Ladies%2520%252B%2520Gentlemen%252C%2520a%2520signed%2520OAuth%2520request%2521'
        test_signing_key = 'kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw&LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE'
        test_signature = 'tnnArxj06cWHq44gCs1OSKk/jLY='
        self.assertEqual(test_signature, oa_calc_signature(test_sig_base_string, test_signing_key))
        
    def test_collect_parameters(self):
        parameters = [
                      ['status','Hello Ladies + Gentlemen, a signed OAuth request!'],
                      ['include_entities','true'],
                      ['oauth_consumer_key','xvz1evFS4wEEPTGEFPHBog'],
                      ['oauth_nonce','kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg'],
                      ['oauth_signature_method','HMAC-SHA1'],
                      ['oauth_timestamp','1318622958'],
                      ['oauth_token','370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb'],
                      ['oauth_version','1.0']
                      ]
        test_parameter_string = 'include_entities=true&oauth_consumer_key=xvz1evFS4wEEPTGEFPHBog&oauth_nonce=kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg&oauth_signature_method=HMAC-SHA1&oauth_timestamp=1318622958&oauth_token=370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb&oauth_version=1.0&status=Hello%20Ladies%20%2B%20Gentlemen%2C%20a%20signed%20OAuth%20request%21'
        self.assertEqual(oa_collect_parameters(parameters), test_parameter_string)
        
    def test_oauth_sign(self):
        parameters = [
                      ['status','Hello Ladies + Gentlemen, a signed OAuth request!'],
                      ['include_entities','true'],
                      ['oauth_consumer_key','xvz1evFS4wEEPTGEFPHBog'],
                      ['oauth_nonce','kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg'],
                      ['oauth_signature_method','HMAC-SHA1'],
                      ['oauth_timestamp','1318622958'],
                      ['oauth_token','370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb'],
                      ['oauth_version','1.0']
                      ]
        test_consumer_secret = 'kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw'
        test_oauth_token_secret = 'LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE'
        test_signature = 'tnnArxj06cWHq44gCs1OSKk/jLY='
        signature = myoauth.oauth_sign('POST', 'https://api.twitter.com/1/statuses/update.json', parameters, test_consumer_secret, test_oauth_token_secret)
        self.assertEqual(test_signature, signature)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()