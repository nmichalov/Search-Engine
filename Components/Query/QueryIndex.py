#!/usr/bin/env python

import os
import re
from gensim import utils
from simserver import SessionServer

class QueryIndex:

    def __init__(self):
        self.service = SessionServer('SearchServer/')

    def query(self, user_query):
        doc = {'tokens': utils.simple_preprocess(user_query)}
        results = self.service.find_similar(doc, min_score=0.4, max_results=50)
        if len(results) > 0:
            for result in results:
                print result[0]
        else:
            print 'No match found'

if __name__ == '__main__':
    queryindex = QueryIndex()
    print 'What are you looking for?'
    user_input = raw_input(': ')
    queryindex.query(user_input)
