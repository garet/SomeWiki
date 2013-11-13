'''
Created on 12 нояб. 2013 г.

@author: garet
'''

from urllib.parse import parse_qsl
from urllib.parse import urlparse
from urllib.parse import unquote


class Url:    
    @staticmethod
    def SplitePath(path):
        result = {}
        index = path.rfind('/')
        if index != -1:
            result['section'] = path[:index + 1]
            result['alias'] = path[index + 1:]
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
        result.update(Url.SplitePath(path))
        return result