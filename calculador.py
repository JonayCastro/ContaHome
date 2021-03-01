# -*- coding:utf-8 -*-

'''
Created on 18 ago. 2018

@author: zeven
'''
import wx

class Sumador(wx.Dialog):            #clase encargada de a�adir nuevos registros
    def __init__(self, parent):
        #super(Sumador, self).__init__()
        self.padre = parent
        self.total = 0
        self.concepto = ''
        self.dato = ''
        wx.Dialog.__init__(self, parent, -1)
        x,y = wx.GetDisplaySize()
        self.SetSize((600,400))
        self.SetTitle('Registro de movimientos en ' + self.padre.nombre.capitalize())
        self.Center()

        panel = wx.Panel(self)

        vbs = wx.BoxSizer(wx.VERTICAL)

        text3 = wx.StaticText(panel, label='Ultimo movimiento')
        self.display3 = wx.TextCtrl(panel, style=wx.TE_READONLY)#ultimo movimiento
        self.display3.SetBackgroundColour(wx.BLACK)
        self.display3.SetForegroundColour(wx.GREEN)
        text1 = wx.StaticText(panel, label='Concepto')
        self.display2 = wx.TextCtrl(panel, style=wx.TE_LEFT)#concepto
        self.display2.SetFocus()
        text2 = wx.StaticText(panel, label='Cantidad')
        self.display1 = wx.TextCtrl(panel, style=wx.TE_RIGHT)#cantidad
        vbs.Add(text3, flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)
        vbs.Add(self.display3, flag=wx.EXPAND|wx.RIGHT|wx.LEFT, border=10)
        vbs.Add(text1, flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)
        vbs.Add(self.display2, flag=wx.EXPAND|wx.RIGHT|wx.LEFT, border=10)
        vbs.Add(text2, flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)
        vbs.Add(self.display1, flag=wx.EXPAND|wx.RIGHT|wx.LEFT|wx.BOTTOM, border=10)
        #esto esta a prueba
        hbs5 = wx.BoxSizer(wx.VERTICAL)
        bcerrar = wx.Button(panel, 9, label='Cerrar', size=(90,28))
        bing = wx.Button(panel, 11, label='Ingresos', size=(90,28))
        bgas = wx.Button(panel, 12, label='Gastos', size=(90,28))
        bbor = wx.Button(panel, 13, label='Borrar', size=(90,28))
        
        hbs5.Add(bing, flag=wx.TOP | wx.EXPAND, border=5)
        hbs5.Add(bgas, flag=wx.TOP | wx.EXPAND, border=5)
        hbs5.Add(bbor, flag=wx.TOP | wx.EXPAND, border=20)
        hbs5.Add(bcerrar, flag=wx.EXPAND | wx.TOP, border=30)
        vbs.Add(hbs5, flag=wx.ALL | wx.EXPAND, border=5)
        #-----------------
        
        '''
        hbs5 = wx.BoxSizer(wx.HORIZONTAL)
        bcerrar = wx.Button(panel, 9, label='Cerrar')
        bing = wx.Button(panel, 11, label='Ingresos')
        bgas = wx.Button(panel, 12, label='Gastos')
        hbs5.Add(bcerrar)
        hbs5.Add(bing)
        hbs5.Add(bgas)
        vbs.Add(hbs5, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=5)

        gsizer = wx.GridSizer(4, 4)            #creamos una grilla con la distribucion de las teclas numericas,
        for row in (("7", "8", "9", "/"),        #simbolos de operaciones, punto y borrar
                    ("4", "5", "6", "*"),
                    ("1", "2", "3", "-"),
                    ("0", ".", 'Borrar', "+")):
            for label in row:
                b = wx.Button(panel, -1, label)
                gsizer.Add(b, flag=wx.ALL, border=2)
        vbs.Add(gsizer, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.bigual = wx.Button(panel, label='=')
        vbs.Add(self.bigual, flag=wx.ALL|wx.EXPAND, border=10)
        '''
        panel.SetSizer(vbs)

        self.Bind(wx.EVT_BUTTON, self.butClic)
        self.Bind(wx.EVT_KEY_UP, self.buTec)
    def buTec(self, event):
        tecla = event.GetKeyCode()
        if tecla == 13:
            n = self.display1.GetValue().rstrip('=')
            if ',' in n:
                n = str(n).replace(',', '.')        #este condicional reemplaza la coma ',' por punto '.'
            if ' ' in n:
                n = str(n).replace(' ', '')         #este condicional elimina los espacios en blanco
            try:
                self.total = eval(n)
                self.display1.SetValue(str(self.total))
            except SyntaxError:
                wx.LogError('Revise los c�lculos')
                return
            except NameError:
                wx.LogError('Expresi�n erronea')
    def butClic(self, event, boton=''):
        boton = event.GetEventObject().GetLabel()
        if boton != 'Ingresos' and boton != 'Gastos' and boton != 'Cerrar':
            self.display1.AppendText(str(boton))
        if boton == '=':
            n = self.display1.GetValue().rstrip('=')
            if ',' in n:
                n = str(n).replace(',', '.')        #este condicional reemplaza la coma ',' por punto '.'
            if ' ' in n:
                n = str(n).replace(' ', '')         #este condicional elimina los espacios en blanco
            try:
                self.total = eval(n)
                self.display1.SetValue(str(self.total))
            except SyntaxError:
                wx.LogError('Revise los c�lculos')
                return
            except NameError:
                wx.LogError('Expresi�n erronea')
        elif boton == 'Borrar':
            self.display1.Clear()
            self.display2.Clear()
        elif boton == 'Cerrar':
            self.Destroy()
            self.padre.libro.NoAs()         #esta linea hace que actualize la informacion mostrada en la ventana principal al cerrar el sumador
        elif boton == 'Ingresos' or boton == 'Gastos':
            con = (self.display2.GetValue()).lower()
            con = con.encode('utf-8')
            if con == '':
                vasio = wx.MessageDialog(self, 'Debe especificar alg�n concepto', style=wx.OK|wx.ICON_EXCLAMATION)
                vasio.ShowModal()
            else:
                self.concepto = self.display2.GetValue()
                self.concepto = self.concepto.strip(' ').encode('utf-8')
                canti = self.display1.GetValue()
                try:
                    if ',' in str(canti):
                        canti = str(canti).replace(',', '.')    #este condicional reemplaza la coma ',' por punto '.'
                    if ' ' in str(canti):
                        canti = str(canti).replace(' ', '')     #este condicional elimina los espacios en blanco
                    if not str(canti).isdigit():            #este condicional evita que se pasen operaciones sin resolver, que puede
                        canti = eval(canti)                 #provocar una perdida de todos los registros
                    if boton == 'Ingresos':
                        self.dato = 'ingresos'
                    elif boton == 'Gastos':
                        self.dato = 'gastos'
                    d = datos.Datos(self.padre.nombre, self.dato, (self.concepto).lower(), canti)
                    esta = d.existe_concep()
                    if esta:
                        ventana = wx.MessageDialog(self, 'El concepto ya existe. �Modificarlo?', style=wx.YES_NO|wx.ICON_QUESTION)
                        res = ventana.ShowModal()
                        if res == wx.ID_YES:
                            d.mod_valor()
                            self.display3.Clear()
                            self.display3.AppendText('Tipo: %s|Concepto: %s|Cantidad: %s' % ((self.dato).capitalize(), (self.concepto).capitalize(), str(canti)))
                            self.padre.libro.NoAs()         #con esta linea se actualiza la informacion mostrada al hacer o modificar un registro
                            self.display1.Clear()
                            self.display2.Clear()
                    else:
                        self.display3.Clear()
                        self.display3.AppendText('Tipo: %s|Concepto: %s|Cantidad: %s' % ((self.dato).capitalize(), (self.concepto).capitalize(), str(canti)))
                        self.padre.libro.NoAs()         #con esta linea se actualiza la informacion mostrada al hacer o modificar un registro
                        self.display1.Clear()
                        self.display2.Clear()
                    self.dato = ''
                    self.total = 0
                    self.concepto = ''
                    self.display2.SetFocus()
                except:
                    wx.MessageBox('Cantidad erronea')