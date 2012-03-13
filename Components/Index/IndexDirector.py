#!/usr/bin/env python

import Pyro4
import threading
from SearchServer import IndexContent

class IndexThread(threading.Thread):
    
    def __init__(self, nameserver, indexer_ident):
        threading.Thread.__init__(self)
        indexer_uri = nameserver.lookup('IndexContent'+indexer_ident)
        self.indexer = Pyro4.Proxy(indexer_uri)
        self.indexer_ident = indexer_ident

    def run(self):
        self.indexer.generate_index()

class IndexData:
    
    def __init__(self):
        ns_host = raw_input('enter nameserver ip: ')
        self.indexer_count = int(raw_input('Enter number of indexers: '))
        self.ns = Pyro4.naming.locateNS(ns_host)
        
    def begin(self):
        for i in range(self.indexer_count):
            indexer = IndexThread(self.ns, str(i))
            indexer.start()

if __name__ == "__main__":
    indexdata = IndexData()
    indexdata.begin()
            
