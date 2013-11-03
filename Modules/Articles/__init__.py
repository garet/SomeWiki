'''
Created on 01 нояб. 2013 г.

@author: garet
'''

from SomeWiki.Base import * 
from SqlMaker import *


class Article_Model:
    def Add(self, page_id, index, data, user_id=-1, user_ip=-1):
        pass

    def Get(self, page_id, index, revision=None):
        pass

    def Delete(self, page_id, index):
        pass


class Article(Controller):
    def __init__(self):
        self.model = Article_Model()

    def View(self, page_id, index, revision=None):
        data = self.model.Get(page_id, index, revision)
        return self.Render('viev.tpl', data)

