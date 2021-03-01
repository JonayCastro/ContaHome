#!/usr/bin/env python
#-*- coding: utf-8 -*-

import MySQLdb, os, datetime
'''
Created on 30 jul. 2018

@author: Jonay Zevanzui Castro Suárez
'''

class DataBase(object):
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'bmwf800st'
        self.conex = ''
        self.cursor = ''
    #conexion
    def db_conex_up(self):
        try:
            self.conex = MySQLdb.connect(self.host, self.user, self.password)
            self.cursor = self.conex.cursor()
            return True #se ha establecido la conexion
        except MySQLdb.Error, e:
            
            return False#no se establecio conexion
    def db_conex_down(self):
        self.cursor.close()
        self.conex.close()
    #---------------------------
    #base de datos 
    def db_create(self):
        try:
            self.cursor.execute('create database conta_home;')
            self.conex.commit()
            return True
        except MySQLdb.Error, e:
            return False
    def db_eraser(self):
        try:
            self.cursor.execute('drop database conta_home;')
            self.conex.commit()
            return True
        except MySQLdb.Error, e:
            return False
    #--------------------------
    #tablas
    def table_create(self):
        table_names = ('ingresos', 'gastos')
        try:
            self.cursor.execute('use conta_home;')
            for i in table_names:
                self.cursor.execute('create table %s (id INT(255) NOT NULL AUTO_INCREMENT, cuenta VARCHAR(125), year INT(4), mes VARCHAR(20), concepto VARCHAR(125), importe DECIMAL(10,2), fecha DATE, PRIMARY KEY (id));' % i)
            self.conex.commit()
            return True
        except MySQLdb.Error, e:
            return False
    #----------------------
    #datos
    def add_data(self, tipo, cuenta, year, mes, concepto, importe ):
        try:
            self.cursor.execute('use conta_home;')
            self.cursor.execute('INSERT INTO %s (cuenta, year, mes, concepto, importe)VALUES (\'%s\', %i, \'%s\', \'%s\', %.2f);' % (tipo, cuenta, year, mes, concepto, importe))
            self.conex.commit()
            return True
        except MySQLdb.Error, e:
            return False
        
    def get_months(self):
        months_list = []
        
        self.cursor.execute('use conta_home;')
        try:
            self.cursor.execute('select distinct mes from gastos union select distinct mes from ingresos;    ')
            r = self.cursor.fetchall()
            for i in r:
                months_list.append(i[0])
            return months_list
        except MySQLdb.Error, e:
            return False
    def get_years(self):
        years_list = []
        self.cursor.execute('use conta_home;')
        try:
            self.cursor.execute('select distinct year from gastos union select distinct year from ingresos;')
            r = self.cursor.fetchall()
            for i in r:
                years_list.append(str(i[0]))
            return years_list
        except MySQLdb.Error, e:
            return False
    def get_counts(self):
        counts_list = []
        
        self.cursor.execute('use conta_home;')
        try:
            self.cursor.execute('select distinct cuenta from gastos union select distinct cuenta from ingresos;')
            r = self.cursor.fetchall()
            for i in r:
                counts_list.append(i[0])
            return counts_list
        except MySQLdb.Error, e:
            return False
     
    def get_quest(self, query):
        
        list_datos = []
        d = []
        if query[1]:
            cuenta = 'cuenta='+ '\''+ query[1] + '\''
            d.append(cuenta)
        if query[2]: 
            year = 'year='+query[2]
            d.append(year)
        if query[3]:
            mes = 'mes='+ '\''+ query[3]+ '\''
            d.append(mes) 
        if len(query[4]) != 0:
            concepto = 'concepto like '+ '(\'%'+ query[4]+ '%\')'
            d.append(concepto)
            
        if query[5] == 0:
            orden = 'asc'
        else:
            orden = 'desc'
            
        q1 = ' and '.join(d)
        q0 = 'select * from %s where %s order by year %s;' % (query[0], q1, orden)
        if len(d) != 0:
            quest = q0
        else:
            quest = 'select * from %s order by year %s;' % (query[0], orden)
            
        self.cursor.execute('use conta_home;')
        try:
            self.cursor.execute(quest)
            r = self.cursor.fetchall()
            for h in r:
                list_datos.append(h)
            return  list_datos
        except MySQLdb.Error, e:
            return False  
       
    
        
        
#d = DataBase()
#d.db_conex_up()
#d.get_all_datas('gastos')
#d.db_conex_down()



