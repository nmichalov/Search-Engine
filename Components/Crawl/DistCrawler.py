#!/usr/bin/env python

import urlparse
import urllib2
import mechanize
import re
import sys
import Pyro4
from BeautifulSoup import BeautifulSoup
from time import sleep
from DataReduce import DataReduce

class Crawler:

    def __init__(self):
        self.datareduce = DataReduce()
        self.visited = []
        self.internal_urls = []
        self.br = mechanize.Browser()
        self.br.addheaders = [('user-agent', 'https://github.com/nmichalov')]

    def crawl(self, target):
        self.visited.append(target)
        current_url_parts = urlparse.urlparse(target)
        try:
            response = self.br.open(target)
        except urllib2.HTTPError, error:
            pass
        else:
            soup = BeautifulSoup(response)
            page_content = soup.findAll('p')
            for p_tag in page_content:
                p_tag = re.sub('\<\/?p\>|\<a href.*\<\/a\>', '', str(p_tag))
                p_tag = re.sub('\<\/?[a-zA-Z0-9]+\>', '', p_tag)
                p_tag = re.sub('[^A-Za-z]', ' ', p_tag)
                self.datareduce.reduce_content('Content#%s#%s' % (target, p_tag.lower())) 
            for link in list(self.br.links()):
                if '@' not in link.url and '?' not in link.url and '#' not in link.url:
                    link_parts =  urlparse.urlparse(link.url)
                    if not bool(link_parts.netloc) or link_parts.netloc == current_url_parts.netloc:
                        link = 'http://'+current_url_parts.netloc+link_parts.path
                        if link not in self.visited and link not in self.internal_urls:
                            self.internal_urls.append(link)
                    else:
                        link = 'http://%s' % (urlparse.urlparse(link.url).netloc)
                        self.datareduce.reduce_links(link)
                        
            sleep(1)
        if len(self.internal_urls) > 0:
            next_target = self.internal_urls.pop()
            self.crawl(next_target)
        else:
            self.datareduce.return_urls()


if __name__ == '__main__':
    hostname = raw_input('enter host ip: ')
    crawler = Crawler()
    Pyro4.Daemon.serveSimple(
            {
                crawler: 'Crawler'
            },
            host = hostname,
            ns = True, verbose = True)
