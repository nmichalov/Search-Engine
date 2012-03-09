#!/usr/bin/env python

import os
import re
from gensim import utils
from simserver import SessionServer


class IndexContent:

    def __init__(self):
        self.service = SessionServer('SearchServer/')
    

    def generate_index(self):
        def page_text():
            for page_file in os.listdir('CrawlData'):
                content = open('CrawlData/'+page_file, 'r')
                page_content = content.read()
                content.close()
                page_url = re.sub('\s', '/', page_file)
                yield page_url, page_content
        corpus = [{'id': '%s' % url, 'tokens': utils.simple_preprocess(text)}
                for url, text in page_text()]
        self.service.train(corpus, method='lsi')
        self.service.index(corpus)


#    def add_new_doc(self, new_doc):
 #       doc_name = re.sub('\s', '/', new_doc)
  #      self.service.index({'id': doc_name, 'tokens': utils.simple_preprocess(new_doc))



if __name__ == '__main__':
    indexcontent = IndexContent()
