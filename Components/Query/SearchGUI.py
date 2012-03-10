#!/usr/bin/env python

from Tkinter import *
from QueryIndex import QueryIndex

def search_index():
    queryindex = QueryIndex()
    user_query =  app_entry.get()
    queryindex.query(user_query)

class Textbox(Frame):
    
    def __init__(self, parent, msg):
        Frame.__init__(self, parent)

        self.g_label = Label(self, text=msg)
        self.g_label.pack(side=LEFT, expand=False)

        self.g_entry = Entry(self)
        self.g_entry.pack(side=LEFT, fill=X, expand=True)

        self.pack(fill=X, anchor=NW, expand=True)

    def text(self):
        return self.g_entry.get()

if __name__ == '__main__':
    newin = Textbox(window, 'Query:')
