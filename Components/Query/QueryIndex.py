#!/usr/bin/env python

import os
import re
import Pyro4
from gensim import utils
from simserver import SessionServer

class QueryIndex:

    def __init__(self):
        self.service = SessionServer('SearchServer/')
        self.search_results = []

    def query(self, user_query):
        doc = {'tokens': utils.simple_preprocess(user_query)}
        results = self.service.find_similar(doc, min_score=0.4, max_results=50)
        self.search_results = results

    def return_results(self):
        return self.search_results

if __name__ == '__main__':
    hostname = raw_input('enter host ip: ')
    ident = raw_input('enter query index identifier: ')
    queryindex = QueryIndex()
    Pyro4.Daemon.serveSimple(
            {
                queryindex: 'QueryIndex%s' % (ident)
            },
            host = hostname,
            ns = True, verbose = True)
