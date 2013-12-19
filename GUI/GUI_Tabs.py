import wx
from GUI.GUI_Elements import CustomButton, CustomTextCtrl_readonly

__author__ = 'vitalyantonenko'


class ConsoleTab(wx.Panel):
    """
    This will be the first notebook tab
    """
    #----------------------------------------------------------------------
    def __init__(self, parent, font_size=9):
        """"""

        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.console = CustomTextCtrl_readonly(self, wx.ID_ANY | wx.EXPAND) #size=(235,100)
        font_console = wx.Font(font_size, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.console.SetFont(font_console)

    def get_console(self):
        return self.console


class ControllerTabPanel(wx.Panel):
    """
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             ) #size=(235,100)
        vbox    = wx.BoxSizer(wx.VERTICAL)
        hbox    = wx.BoxSizer(wx.HORIZONTAL)

        self.buttonRemove = CustomButton(self, id=wx.ID_ANY, label="DEL CONTROLLER") #size=(80, 25)
        self.buttonRemove.Bind(wx.EVT_BUTTON, self.onButtonRemove)
        hbox.Add(self.buttonRemove, 1, wx.EXPAND|wx.RIGHT, 1)

        self.buttonInsert = CustomButton(self, id=wx.ID_ANY, label="NEW CONTROLLER") #size=(80, 25)
        self.buttonInsert.Bind(wx.EVT_BUTTON, self.onButtonInsert)
        hbox.Add(self.buttonInsert, 1, wx.EXPAND)

        vbox.Add(hbox, 0, wx.EXPAND)

        self.controller_tabs = wx.Notebook(self)
        vbox.Add(self.controller_tabs, 2, flag=wx.EXPAND)

        self.SetSizer(vbox)

        self.pageCounter = 0
        self.addPage(main=True)

    def addPage(self, main=False):
        self.pageCounter += 1
        page      = ConsoleTab(self.controller_tabs, font_size=7)
        if main:
            pageTitle = "MainCtrl"
        else:
            pageTitle = "Ctrl: {0}".format(str(self.pageCounter))
        self.controller_tabs.AddPage(page, pageTitle)

    def onButtonRemove(self, event):
        page_index = self.controller_tabs.GetSelection()
        if page_index != 0:
            self.controller_tabs.DeletePage(page_index)

    def onButtonInsert(self, event):
        self.addPage()

    def get_console(self):
        return self.controller_tabs.GetCurrentPage().get_console()


class ConsoleTabPanel(wx.Panel):
    """
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             ) #size=(235,100)
        vbox    = wx.BoxSizer(wx.VERTICAL)
        hbox    = wx.BoxSizer(wx.HORIZONTAL)

        self.buttonRemove = CustomButton(self, id=wx.ID_ANY, label="DEL CONSOLE") #size=(80, 25)
        self.buttonRemove.Bind(wx.EVT_BUTTON, self.onButtonRemove)
        hbox.Add(self.buttonRemove, 1, wx.EXPAND|wx.RIGHT, 1)

        self.buttonInsert = CustomButton(self, id=wx.ID_ANY, label="NEW CONSOLE") #size=(80, 25)
        self.buttonInsert.Bind(wx.EVT_BUTTON, self.onButtonInsert)
        hbox.Add(self.buttonInsert, 1, wx.EXPAND)

        vbox.Add(hbox, 0, wx.EXPAND)

        self.console_tabs = wx.Notebook(self)
        vbox.Add(self.console_tabs, 2, flag=wx.EXPAND)

        self.SetSizer(vbox)

        self.pageCounter = 0
        self.addPage(main=True)

    def addPage(self, main=False):
        self.pageCounter += 1
        page      = ConsoleTab(self.console_tabs)
        if main:
            pageTitle = "MainCon"
        else:
            pageTitle = "Con: {0}".format(str(self.pageCounter))
        self.console_tabs.AddPage(page, pageTitle)

    def onButtonRemove(self, event):
        page_index = self.console_tabs.GetSelection()
        if page_index != 0:
            self.console_tabs.DeletePage(page_index)

    def onButtonInsert(self, event):
        self.addPage()

    def get_console(self):
        return self.console_tabs.GetCurrentPage().get_console()