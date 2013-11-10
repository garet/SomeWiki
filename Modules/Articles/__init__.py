'''
Created on 01 нояб. 2013 г.

@author: garet
'''

from SomeWiki.Base import * 
from SqlMaker import *
import psycopg2

class Article_Model:
    def __init__(self, db):
        self.__db = db
        
    def CheckArticleRelative(self, page_id, index):
        self.__db.Select()
        self.__db.From('{pref}articles_relative')
        self.__db.Where('artrel_page_id={ph}', page_id)
        self.__db.Where('artrel_index={ph}', index)
        if self.__db.Execute(commite=False) == False:
            raise Exception('Article_Model: Can`t check article!')
        return self.__db.FetchOne()

    # Complite
    def NewArticle(self, status=-1, permission=-1):
        self.__db.Insert('{pref}articles',
                         {'article_first_id': -1},
                         {'article_last_id': -1},
                         {'article_status': status},
                         {'article_permission': permission})
        self.__db.AddReturnId('article_id')
        if self.__db.Execute(commite=False) == False: 
            raise Exception('Article_Model: Can`t add new article!')
        return self.__db.InsertId()

    # Complite
    def UpdateArticleTexts(self, last_id, first_id=None):
        if first_id != None:
            self.__db.Update('{pref}articles',
                             {'article_first_id': first_id},
                             {'article_last_id': last_id})
        else:
            self.__db.Update('{pref}articles', {'article_last_id': last_id})
        if self.__db.Execute(commite=False) == False: 
            raise Exception('Article_Model: Can`t update article text id!')

    def NewArticleRelative(self, page_id, index, article_id):
        self.__db.Insert('{pref}articles_relative',
                         {'artrel_page_id': page_id},
                         {'artrel_article_id': article_id},
                         {'artrel_index': index},
                         {'artrel_status': 0},
                         {'artrel_permission': 0})
        if self.__db.Execute(commite=False) == False: 
            raise Exception('Article_Model: Can`t add new article relative!')

    def NewArticleText(self, article_id, revision, source, result, user_id, user_ip):
        self.__db.Insert('{pref}articles_texts',
                         {'text_article_id': article_id},
                         {'text_revision': revision},
                         {'text_source': source},
                         {'text_result': result},
                         {'text_user_id': user_id},
                         {'text_user_ip': user_ip},
                         {'text_date_add': SqlFuncs.Now})
        self.__db.AddReturnId('text_id')
        if self.__db.Execute(commite=False) == False: 
            raise Exception('Article_Model: Can`t add new article relative!')
        return self.__db.InsertId()
        
    def Add(self, page_id, index, data, user_id=-1, user_ip=-1):
        # Accept all previous changes.
        self.__db.Commite()
        try:
            # Check exist article
            article = self.__CheckArticleRelative(page_id, index)
            # If article not exist then create new article
            if article == False:
                pass
            # Else add new revision
            else:
                pass
            pass
        except Exception as e:
            self.__db.Rollback()
            return False

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


conn = psycopg2.connect(database="SomeWiki", user="garet", password="joker12")
obj = SqlMaker(conn=conn, type_db='pg', pref='tbl_', debug=True)

model = Article_Model(obj)
article_id = model.NewArticle()
print(article_id)
text_id = model.NewArticleText(0, 0, 'source text', 'result text', -1, -1)
print(text_id)
model.UpdateArticleTexts(text_id, text_id)

obj.Select()
obj.From('{pref}articles')
obj.Where('article_id={ph}', article_id)
obj.Execute()
print(obj.FetchOne())

#param = SqlFuncs.Now
#print(type(param))
#print(param)