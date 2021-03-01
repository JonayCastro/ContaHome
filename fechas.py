'''
Created on 7 ago. 2018

@author: zeven
'''

import datetime

class Fechas(object):
    
    def get_month(self):
        mes = None
        meses = {1:'enero', 2:'febrero', 3:'marzo', 4:'abril',
                 5:'mayo', 6:'junio', 7:'julio', 8:'agosto',
                 9:'septiembre', 10:'octubre', 11:'noviembre', 12:'diciembre'}
        a = datetime.datetime.now()
        m = a.month
        y = a.year
        for c,v in meses.iteritems():
            if m == c:
                mes = v
        return mes, y

    def get_date(self):
        formato = "%d-%m-%y %I:%m %p"
        hoy = datetime.datetime.today()
        fecha = hoy.strftime(formato)
        
        return fecha
 
 
f = Fechas()
f.get_month()       