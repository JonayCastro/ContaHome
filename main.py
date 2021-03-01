#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx, os, wx.grid
from db import DataBase as DB
from fechas import Fechas as FE
from calculador import Sumador as SUM
'''
Created on 2 ago. 2018

@author: Jonay Zevenzui Castro Suárez
'''

PATH_JOIN = None
PATH_CWD = None


class Salida(wx.grid.Grid):
    def __init__(self, parent):
       
        wx.grid.Grid.__init__(self, parent, -1)
        self.EnableEditing(False)
        
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.cell_right_click)
    
    def make_grid(self):
        encabezados = ('Id', 'Cuenta', 'Año', 'Mes', 'Concepto', 'Importe', 'Fecha')
        self.CreateGrid(1000, 7)
                
        self.SetColSize(0, 40)
        self.SetColSize(1, 100)
        self.SetColSize(2, 80)
        self.SetColSize(3, 100)
        self.SetColSize(4, 730)
        self.SetColSize(5, 100)
        self.SetColSize(6, 120)
        
        for i,c in enumerate(range(len(encabezados))):
            self.SetColLabelValue(c, encabezados[i])
            
        return self    
    
    def cell_right_click(self, e):
        grid_name = e.GetEventObject().GetName()
        row, coll = e.GetRow(), e.GetCol()
        

class Libro(wx.Notebook):
    def __init__(self, parent):
        self.h = []
        wx.Notebook.__init__(self, parent, -1)
    def set_book(self):
        book_name = ('ingresos', 'gastos')
        
        for i in book_name:
            
            s = Salida(self)
            hoja = s.make_grid()
            hoja.SetName(i)
            self.h.append(hoja)
            
        
        for i in self.h:
            self.AddPage(i, i.GetName().capitalize())
        
        
class Gui(wx.Frame):
    def __init__(self):
        
        f = FE()
        self.mes, self.year = f.get_month()
        self.choices = []
        
        wx.Frame.__init__(self, None)
        
        x,y = wx.GetDisplaySize()
        #self.SetSize((x,y))
        self.SetSize((800,500))
        self.Center()
        self.SetTitle('Conta_home')
        
        #-------------sizers------------------------------
        prin_sizer = wx.BoxSizer(wx.VERTICAL)
        herr_sizer = wx.BoxSizer(wx.HORIZONTAL)
        choice_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #-------------------------------------------------
        #------------notebook-----------------------------
        self.books = Libro(self)
        #-------------------------------------------------
        #-----------herramientas--------------------------
        self.button_add = wx.BitmapButton(self, 8,  size=(40,40), bitmap=wx.Bitmap('icons/sumar.png'))
        
        #-------------------------------------------------
        #--------selectores-------------------------------
        text_counts_selec = wx.StaticText(self, -1, 'Cuenta: ')
        self.counts_choice = wx.Choice(self, 10)
        self.choices.append(self.counts_choice)
        
        text_year_select = wx.StaticText(self, -1, 'Año: ')
        self.year_choice = wx.Choice(self, 11)
        self.choices.append(self.year_choice)
        
        text_months_select = wx.StaticText(self, -1, 'Mes: ')
        self.months_choice = wx.Choice(self, 12)
        self.choices.append(self.months_choice)
                
        self.search = wx.TextCtrl(self, -1)
        self.search.SetHint('Buscar concepto...')
        
        text_orden = wx.StaticText(self, -1, 'Orden: ')
        self.orden_choice = wx.Choice(self, 15)
        lista_orden = ('Ascendente', 'Descendente')
        self.orden_choice.AppendItems(lista_orden)
        self.orden_choice.SetSelection(0)

        self.but_search = wx.Button(self, 13, 'Buscar')
        
        self.but_reset = wx.Button(self, 14, 'Reset')
        #-------------------------------------------------
        
        herr_sizer.Add(self.button_add, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        
        choice_sizer.Add(text_counts_selec, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        choice_sizer.Add(self.counts_choice, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        choice_sizer.Add(text_year_select, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        choice_sizer.Add(self.year_choice, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        choice_sizer.Add(text_months_select, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        choice_sizer.Add(self.months_choice, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        choice_sizer.Add(self.search, proportion=1, flag=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=5)
        choice_sizer.Add(text_orden, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        choice_sizer.Add(self.orden_choice, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        choice_sizer.Add(self.but_search, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        choice_sizer.Add(self.but_reset, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        
        prin_sizer.Add(choice_sizer, flag=wx.EXPAND|wx.ALL, border=5)
        prin_sizer.Add(herr_sizer, flag=wx.ALL|wx.EXPAND, border=5)
        prin_sizer.Add(self.books,proportion=1,flag=wx.EXPAND|wx.ALL, border=5)
        
        self.SetSizer(prin_sizer)
        
        self.set_datas()
        
        self.Bind(wx.EVT_BUTTON, self.event_buttons)
        self.Bind(wx.EVT_ACTIVATE, self.event_activate)
        
    def read_db(self, grilla_name):
        query_data = []
        query_data.append(grilla_name)
        for i in range(len(self.choices)):
            if self.choices[i].GetStringSelection() != 'Todas' and self.choices[i].GetStringSelection() != 'Todos':
                query_data.append(self.choices[i].GetStringSelection().lower())
            else:
                query_data.append(False)
        query_data.append(self.search.GetValue())
        query_data.append(self.orden_choice.GetSelection())        
        d = DB()
        if d.db_conex_up():
            datas = d.get_quest(query_data)
            d.db_conex_down()
        return datas   
        
        
    def event_activate(self, e):
        try:
            if self.books.GetPageCount() == 0:
                self.books.set_book()
                for i in self.books.h:
                    datas = self.read_db(i.GetName())
                    i.ClearGrid()
                    
                    for j in range(len(datas)):
                        linea = datas[j]
                        for h in range(len(linea)):
                            i.SetCellValue(j, h, str(linea[h]))
                
        except:
            pass
    
    def event_buttons(self, e):
        id_b = e.GetId()
        if id_b == 14:
            self.counts_choice.SetStringSelection('nomina')
            self.year_choice.SetStringSelection(str(self.year))
            self.months_choice.SetStringSelection(self.mes)
        elif id_b == 13:
            
            for i in self.books.h:
                datas = self.read_db(i.GetName())
                i.ClearGrid()
                for j in range(len(datas)):
                    linea = datas[j]
                    for h in range(len(linea)):
                        i.SetCellValue(j, h, str(linea[h]))
        elif id_b == 8:
            
            print 'add'
            s = SUM(self)
            
             
                
    def set_datas(self):
        base = DB()
        meses = ['Todos', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        if base.db_conex_up():
            count_list =  base.get_counts()
            count_list.insert(0, 'Todas')
            year_list = base.get_years()
            year_list.insert(0, 'Todos')
        base.db_conex_down()
            
        self.counts_choice.AppendItems(count_list)
        self.counts_choice.SetStringSelection('nomina')
        
        self.year_choice.AppendItems(year_list)
        self.year_choice.SetStringSelection(str(self.year))
        
        self.months_choice.AppendItems(meses)
        self.months_choice.SetStringSelection(self.mes)

def get_sistem():
    global PATH_JOIN
    global PATH_CWD
    
    if os.name == 'posix':
        PATH_JOIN = '/'
    else:
        PATH_JOIN = '\\'
    PATH_CWD = os.getcwd()
def main():
    app = wx.App()
    frame = Gui()
    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    get_sistem()
    main()
    
    