import wx

__author__ = 'vitalyantonenko'


class CustomButton(wx.Button):
    def __init__(self, *a, **k):
        style = ( wx.NO_BORDER )
        wx.Button.__init__(self, style=style, *a, **k)

        self.SetBackgroundColour('#B2B2B2') #C4C4FF
        # more customization here


class CustomTextCtrl_readonly(wx.TextCtrl):
    def __init__(self, *a, **k):
        style = ( wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL )
        wx.TextCtrl.__init__(self, style=style, *a, **k)

        self.SetBackgroundColour('#D8D8D8')
        # more customization here


class CustomTextCtrl(wx.TextCtrl):
    def __init__(self, *a, **k):
        style = ( wx.NO_BORDER )
        wx.TextCtrl.__init__(self, style=style, *a, **k)

        self.SetBackgroundColour('#D8D8D8')
        # more customization here