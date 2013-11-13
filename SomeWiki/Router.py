'''
Created on 01 нояб. 2013 г.

@author: garet
'''

import hashlib

import psycopg2

from SqlMaker import SqlMaker
from SomeWiki.Request import Request
from SomeWiki.Urls import Url


class Router:
    def __self(self, db, request):
        self.__db = db
        self.__model = RouterModel()
        self.__request = request
                
    def AddPage(self, url):
        pass


class RouterModel:
    def AddAlias(self, db, alias, commit=True):
        # Select alias
        db.Select('alias_id')
        db.From('{pref}aliases')
        db.Where('alias_name={ph}', alias)
        if db.Execute(commit=False) == False:
            raise Exception('RouterModel: Can`t find alias!')
        # Insert alias
        result = db.FetchOne()
        if result != False:
            return result['alias_id']
        db.Insert('{pref}aliases', {'alias_name': alias})
        db.AddReturnId('alias_id')
        if db.Execute(commit=commit) == False:
            raise Exception('RouterModel: Can`t insert alias!')
        return db.InsertId()

    def AddSection(self, db, section, commit=True):
        # Select section
        db.Select('section_id')
        db.From('{pref}sections')
        db.Where('section_name={ph}', section)
        if db.Execute(commit=commit) == False:
            raise Exception('RouterModel: Can`t find section!')
        # Insert section
        result = db.FetchOne()
        if result != False:
            return result['section_id']
        db.Insert('{pref}sections', {'section_name': section})
        db.AddReturnId('section_id')
        if db.Execute() == False:
            raise Exception('RouterModel: Can`t insert section!')
        return db.InsertId()

    def AddDomen(self, db, domen, commit=True):
        # Select section
        db.Select('domen_id')
        db.From('{pref}domens')
        db.Where('domen_name={ph}', domen)
        if db.Execute(commit=commit) == False:
            raise Exception('RouterModel: Can`t find domen!')
        # Insert section
        result = db.FetchOne()
        if result != False:
            return result['domen_id']
        db.Insert('{pref}domens', {'domen_name': domen})
        db.AddReturnId('domen_id')
        if db.Execute() == False:
            raise Exception('RouterModel: Can`t insert domen!')
        return db.InsertId()
    
    def AddScheme(self, db, scheme_text, commit=True):
        db.Insert('{pref}schemes', {'scheme_text': scheme_text})
        db.AddReturnId('scheme_id')
        if db.Execute(commit=commit) == False:
            raise Exception('RouterModel: Can`t insert scheme!')
        return db.InsertId()
    
    def InsertPage(self, db, domen_id, section_id, alias_id, 
                   scheme_1_id, scheme_2_id, status=-1, permission=-1):
        db.Insert('{pref}pages',
                  {'page_domen_id': domen_id},
                  {'page_section_id': section_id},
                  {'page_alias_id': alias_id},
                  {'page_scheme_1_id': scheme_1_id},
                  {'page_scheme_2_id': scheme_2_id},
                  {'page_status': status},
                  {'page_permission': permission})
        db.AddReturnId('page_id')
        if db.Execute() == False:
            raise Exception('RouterModel: Can`t insert page!')
        return db.InsertId()
    
    def AddPage(self, db, url, scheme_1_id, scheme_2_id, status=-1, permission=-1):
        url_obj = Url.ParseUrl(url)
        try:
            db.Commit()
            domen_id = self.AddDomen(db, url_obj['domen'], commit=False)
            section_id = self.AddSection(db, url_obj['section'], commit=False)
            alias_id = self.AddAlias(db, url_obj['alias'], commit=False)
            page_id = self.InsertPage(db, domen_id, section_id, alias_id, 
                                      scheme_1_id, status, permission)
            return page_id
        except Exception as e:
            db.Rollback()
            raise Exception('RouterModel: Can`t add page!')
        else:
            return {'domen_id': domen_id, 'section_id': section_id,
                    'alaise_id': alias_id, 'page_id': page_id,
                    'domen': url_obj['domen'], 'section': url_obj['section'],
                    'alias': url_obj['alias'], 'url': url}
    
    def UpdateScheme(self, scheme_id, scheme_text):
        pass

conn = psycopg2.connect(host='192.168.100.6', database="SomeWiki", user="garet", password="joker12")
db = SqlMaker(conn=conn, type_db='pg', pref='tbl_', debug=False)


url = 'http://hghltd.yandex.net:888/ывффывор?fmode=inject&url=http%3A%2F%2Fmetro.yandex.ru%2Fmoscow&tld=ru&text=%D0%BA%D0%B0%D1%80%D1%82%D0%B0%20%D0%BC%D0%B5%D1%82%D1%80%D0%BE%20%D0%BC%D0%BE%D1%81%D0%BA%D0%B2%D1%8B&l10n=ru&mime=html&sign=cbab244bf9a8313ebdb1944b0aaa9274&keyno=0&aParam%5B0%5D=1&aParam%5B1%5D=4&aParam%5Ba%5D=b&aParam%5Bc%5D=d'
#url = 'http://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BF%D1%80%D0%BE%D0%B8%D0%B7%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B9_%D0%96%D1%8E%D0%BB%D1%8F_%D0%92%D0%B5%D1%80%D0%BD%D0%B0'
#url = 'http://ru.wikipedia.org/%E0%AA%AA%E0%AB%83%E0%AA%B7%E0%AB%8D%E0%AA%A0%E0%AB%8B%E0%AA%A8%E0%AB%87_%E0%AA%B6%E0%AB%8B%E0%AA%A7%E0%AA%B5%E0%AA%BE_%E0%AA%95%E0%AB%87_%E0%AA%86_%E0%AA%B6%E0%AB%80%E0%AA%B0%E0%AB%8D%E0%AA%B7%E0%AA%95_%E0%AA%B2%E0%AA%BF%E0%AA%82%E0%AA%95.html/'
request = Request(url)

model = RouterModel()
result = model.AddPage(db, url, 0, 0)
print(result)
#m = model.AddAlias(db, request.aliase)
#print('Aliase ID:', m, request.aliase)
#m = model.AddSection(db, request.section)
#print('Section ID:', m, request.section)
#m = model.AddDomen(db, request.domen)
#print('Domen ID:', m, request.domen)
#m = model.AddScheme(db, 'scheme!')
#print('Scheme ID:', m, 'scheme!')



#pop = hashlib.sha512('obaha!'.encode())
#print(pop.hexdigest())
#print(len(pop.hexdigest()))
#print(pop.digest_size)