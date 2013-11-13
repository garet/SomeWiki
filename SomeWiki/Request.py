'''
Created on 11 нояб. 2013 г.

@author: garet
'''

from urllib.parse import parse_qsl
from urllib.parse import urlparse
from urllib.parse import unquote


class Request:
    def __init__(self, url):
        url_obj = Request.ParseUrl(url)
        self.__aliase = url_obj['aliase']
        self.__section = url_obj['section']
        self.__query = url_obj['query']
        self.__params = url_obj['params']
        self.__path = url_obj['path']
        self.__domen = url_obj['domen']
        self.__protocol = url_obj['protocol']
        
    @property
    def aliase(self):
        return self.__aliase

    @property
    def section(self):
        return self.__section
    
    @property
    def query(self):
        return self.__query
    
    @property
    def params(self):
        return self.__params
    
    @property
    def protocol(self):
        return self.__protocol
    
    @property
    def domen(self):
        return self.__domen
    
    @staticmethod
    def SplitePath(path):
        result = {}
        index = path.rfind('/')
        if index != -1:
            result['section'] = path[:index + 1]
            result['aliase'] = path[index + 1:]
        else:
            result['section'] = path
        return result
    
    @staticmethod
    def ParseUrl(url):
        result = {}
        url_obj = urlparse(url)
        path = unquote(url_obj.path)
        result['protocol'] = url_obj.scheme
        result['params'] = parse_qsl(url_obj.query)
        result['domen'] = url_obj.netloc
        result['query'] = url_obj.query
        result['path'] = path
        result.update(Request.SplitePath(path))
        return result