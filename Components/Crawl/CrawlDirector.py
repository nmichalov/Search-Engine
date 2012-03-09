#!/usr/bin/env python

import sys
import Pyro4
import os
import cPickle
import threading

class Director:
    
    def __init__(self):
        self.target_urls = []
        if os.path.exists('Visited.pkl'):
            visited = open('Visited.pkl', 'r')
            self.visited_urls = cPickle.load(visited)
            visited.close()
        else:
            self.visited_urls = []

    def add_new(self, url):
        if url not in self.visited_urls:
            self.target_urls.append(url)
        
    def new_urls(self):
        return self.target_urls

    def update_record(self):
        self.visited_urls.append(self.target_urls)
        visited_list = open('Visited.pkl', 'w')
        cPickle.dump(self.visited_urls, visited_list)
        visited_list.close()

def main():
    ns_host = raw_input('enter nameserver ip: ')
    crawler_count = int(raw_input('enter the number of crawler instances: '))
    director = Director()
    ns = Pyro4.naming.locateNS(ns_host)
    urls = []
    url_file = open('URLlist', 'r')
    for line in url_file:
        line = line.strip()
        director.add_new(line)
    target_urls = director.new_urls()
    batch_size = len(target_urls)/crawler_count
    batch_dict = {}
    for i in range(crawler_count):
        if i < (crawler_count - 1):
            batch_dict[i] = target_urls[i:(i+1)*batch_size]
        else:
            batch_dict[i] = target_urls[i::]
    for i in range(crawler_count):
        print 'Enter identifier for crawler %s' % (str(i))
        crawler_ident = raw_input(': ')
        crawler_uri = ns.lookup('Crawler'+crawler_ident)
        crawler = Pyro4.Proxy(crawler_uri)
        threading.Thread.start(crawler.start_crawl(batch_dict[i]))
    director.update_record()

if __name__ == "__main__":
    main()
