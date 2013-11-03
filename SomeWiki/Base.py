'''
Created on 01 нояб. 2013 г.

@author: garet
'''

from flask import render_template
from config import Config

class Controller:
    template_folder = '/templates/modules'
    def Render(self, template_name, *args):
        return render_template(template_name, args)
    
obj = Config.base_folder