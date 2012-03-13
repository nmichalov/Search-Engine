#!/usr/bin/env python

import os
import re
import Pyro4
from gensim import utils
from simserver import SessionServer


class IndexContent:

    def __init__(self):
        self.service = SessionServer('SearchServer/')
    

    def yield_page_text(self):
        for page_file in os.listdir('CrawlData'):
            content = open('CrawlData/'+page_file, 'r')
            page_content = content.read()
            content.close()
            page_url = re.sub('\s', '/', page_file)
            yield page_url, page_content

    def generate_index(self):
        corpus = [{'id': '%s' % url, 'tokens': utils.simple_preprocess(text)}
                for url, text in self.yield_page_text()]
        self.service.train(corpus, method='lsi')
        self.service.index(corpus)


#    def add_new_doc(self, new_doc):
 #       doc_name = re.sub('\s', '/', new_doc)
  #      self.service.index({'id': doc_name, 'tokens': utils.simple_preprocess(new_doc))



if __name__ == '__main__':
    hostname = raw_input('enter host ip: ')
    ident = raw_input('enter indexer identifier: ')
    indexcontent = IndexContent()
    Pyro4.Daemon.serveSimple(
            {
                indexcontent: 'IndexContent%s' % (ident)
            },
            host = hostname,
            ns = True, verbose = True)
