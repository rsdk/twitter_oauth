'''
Created on 05.08.2012

@author: rene
'''
import unittest
import twitter_connect


class Test(unittest.TestCase):


    def test_add_params(self):
        first = twitter_connect.add_params([['count','5'],['since_id','12345'],['include_entities','true']])
        second = '?count=5&since_id=12345&include_entities=true'      
        self.assertEqual(first, second)
        
    def test_hashtagsfinden(self):
        first = twitter_connect.hashtagsfinden('der kleine #hund isst das #steak doch #nicht')
        second = ['hund','steak','nicht']
        self.assertEqual(first, second)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()