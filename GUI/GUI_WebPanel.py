import os
import subprocess
import networkx as nx
import pexpect
import wx
import sys

from wx import html2 as webview
from config.config_constants import CONTROLLER_PATH
from src.KThread import KThread




class WebPanel(wx.Panel):
    """Class fo WebPanel.

    TODO
    """
    def __init__(self, parent):
        '''Cunstructor of WebPanel.

        Args:
            parent:

        '''
        self.p = None
        wx.Panel.__init__(self, parent)

        self.current = os.path.realpath(parent.parent.html_path)
        self.frame = parent
        if parent:
            self.titleBase = parent.GetTitle()

        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.wv = webview.WebView.New(self)

        self.contentNotSaved = True


        btn = CustomButton(self, -1, "Simulate")
        # btn.SetBackgroundColour('#93FF8C') B2B2B2
        self.Bind(wx.EVT_BUTTON, self.OnSimulateButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.RIGHT, 1)

        btn = CustomButton(self, -1, "DB:JSON")
        btn.SetBackgroundColour('#B5B5B5')
        self.Bind(wx.EVT_BUTTON, self.OnDBJsonButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.RIGHT, 1)

        btn = CustomButton(self, -1, "Random")
        self.Bind(wx.EVT_BUTTON, self.OnRandomButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND)

        self.node_num = CustomTextCtrl(self, size=(117, -1))
        self.node_num.ChangeValue(str(17))
        btnSizer.Add(self.node_num, 0, wx.EXPAND)

        btn = CustomButton(self, -1, "Save")
        self.Bind(wx.EVT_BUTTON, self.OnSaveButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.LEFT, 420)

        btn = CustomButton(self, -1, "Load")
        self.Bind(wx.EVT_BUTTON, self.OnLoadButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.LEFT, 1)

        sizer.Add(btnSizer, 0, wx.EXPAND)
        sizer.Add(self.wv, 1, wx.EXPAND)

        self.console = CustomTextCtrl_readonly(self, wx.ID_ANY, size=(235,100))
        font_console = wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.console.SetFont(font_console)

        self.controller = CustomTextCtrl_readonly(self, wx.ID_ANY, size=(235,100))
        font_controller = wx.Font(7, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.controller.SetFont(font_controller)

        btn = CustomButton(self, wx.ID_ANY, 'Send')
        self.Bind(wx.EVT_BUTTON, self.onSendButton, btn)

        self.cmd_line = CustomTextCtrl(self, wx.ID_ANY, size=(235,-1))
        font_cmd_line = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.cmd_line.SetFont(font_cmd_line)
        self.cmd_line.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)

        # Add widgets to a sizer
        con_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        con_hsizer.Add(self.cmd_line, 0, wx.EXPAND)
        con_hsizer.Add(btn, 1, wx.EXPAND)

        con_sizer = wx.BoxSizer(wx.VERTICAL)
        con_sizer.Add(self.controller, 1, wx.BOTTOM|wx.EXPAND, 1)
        con_sizer.Add(self.console, 2, wx.ALL|wx.EXPAND)
        con_sizer.Add(con_hsizer, 0, wx.ALL|wx.CENTER)

        glob_sizer = wx.BoxSizer(wx.HORIZONTAL)
        glob_sizer.Add(con_sizer, 0, wx.EXPAND)
        glob_sizer.Add(sizer, 1, wx.EXPAND)

        self.SetSizer(glob_sizer)
        self.wv.LoadURL('file://' + self.current)

    def onKeyPress(self, event):
        keycode = event.GetKeyCode()
        if keycode == 13: # ENTER KEY
            self.onSendButton(event)
        event.Skip()

    def onSendButton(self, event):
        # cmd = self.cmd_line.GetValue()
        # if cmd != 'exit':
        #     self.p.sendline(cmd)
        #     self.p.expect('mininet CE> ')
        #     for s in self.p.before:
        #         if len(s) != 0 and s != '\n':
        #             self.console.AppendText(s)
        #     self.cmd_line.ChangeValue('')
        # else:
        #     self.p.sendline(cmd)
        #     self.p.expect(pexpect.EOF)
        #     for s in self.p.before:
        #         if len(s) != 0 and s != '\n':
        #             self.console.AppendText(s)
        #     self.cmd_line.ChangeValue('')
        #     self.controller_thread.kill()
        #     self.controller_proc.terminate()

        cmd = self.cmd_line.GetValue()
        if cmd != 'exit':
            self.console_proc.stdin.write(cmd + '\n')
            self.cmd_line.ChangeValue('')
        else:
            self.console_proc.stdin.write(cmd + '\n')
            #self.console_thread.kill()
            self.cmd_line.ChangeValue('')
            self.controller_thread.kill()
            self.controller_proc.terminate()

    def OnLoadButton(self, event):
        if self.contentNotSaved:
            if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
                             wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return
        openFileDialog = wx.FileDialog(self, "Open MNCE Graph file", "", "",
                                       "MNCE Graph files (*.mnce)|*.mnce", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        input_stream = wx.FileInputStream(openFileDialog.GetPath())
        if not input_stream.IsOk():
            wx.LogError("Cannot open file '%s'."%openFileDialog.GetPath())
            return

    def OnSaveButton(self, event):
        saveFileDialog = wx.FileDialog(self, "Save MNCE Graph file", "", "",
                                   "MNCE Graph files (*.mnce)|*.mnce", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        output_stream = wx.FileOutputStream(saveFileDialog.GetPath())
        if not output_stream.IsOk():
            wx.LogError("Cannot save current contents in file '%s'."%saveFileDialog.GetPath())
            return

    def OnSimulateButton(self, event):
        os.system("cp GUI/res/not_ready.png GUI/result.png")
        # Save current graph
        self.console.ChangeValue('')
        self.controller.ChangeValue('')
        prev_title = self.wv.GetCurrentTitle()
        self.wv.RunScript("document.title = my_graph_editor.export_sage()")
        graph_data = self.wv.GetCurrentTitle()
        self.wv.RunScript("document.title = %s" % prev_title)
        # p = self.GetParent()
        # p.set_graph_data(graph_data)

        controller_cmd = "java -jar " + CONTROLLER_PATH + "/target/floodlight.jar"
        self.controller_proc = subprocess.Popen(controller_cmd, stdout=subprocess.PIPE, shell=True)
        self.controller_thread = KThread(target=self.controller_thread_func)
        self.controller_thread.setDaemon(True)
        self.controller_thread.start()
        #self.controller.AppendText("CONTROLLER ON")

        # self.p = pexpect.spawn(sys.prefix + '/bin/python main.py \'' + graph_data + '\'', timeout=777)
        #
        # self.p.expect('mininet CE> ') #mininet CE>
        # for s in self.p.before:
        #     if len(s) != 0 and s != '\n':
        #         self.console.AppendText(s)

        console_cmd = sys.prefix + '/bin/python main.py \'' + graph_data + '\''
        self.console_proc = subprocess.Popen(console_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        self.console_thread = KThread(target=self.console_thread_func)
        self.console_thread.setDaemon(True)
        self.console_thread.start()


    def OnDBJsonButton(self, event):
        prev_title = self.wv.GetCurrentTitle()
        self.wv.RunScript("document.title = my_graph_editor.export_sage()")
        graph_data = self.wv.GetCurrentTitle()
        self.wv.RunScript("document.title = %s" % prev_title)
        # graph_data = cookies.split('=')[1]
        # print(graph_data)
        print(graph_data)
        # p = self.GetParent()
        # p.set_graph_data(graph_data)

    def OnRandomButton(self, event):
        raw_value = self.node_num.GetValue().strip()
        # numeric check
        if all(x in '0123456789.+-' for x in raw_value):
            # convert to float and limit to 2 decimals
            value = round(float(raw_value), 2)
            self.node_num.ChangeValue(str(value))
            G = nx.barabasi_albert_graph(value, 1, 777)
            js_str = self.import_from_networkx_to_json(G)
            self.wv.RunScript("jrg = '%s'" % js_str)
            self.wv.RunScript("my_graph_editor.import_from_JSON(jrg)")
        else:
            self.node_num.ChangeValue("Number only")

    def import_from_networkx_to_json(self, G):
        pos = nx.spring_layout(G)
        js_data = {}
        js_data["vertices"] = []
        js_data["pos"] = {}
        for n in G.nodes():
            js_data["vertices"].append(str(n))
            js_data["pos"][str(n)] = [pos[n][0], pos[n][1]]
        js_data["edges"] = []
        for e in G.edges():
            js_data["edges"].append([str(e[0]), str(e[1]), None])
        js_data["name"] = "G"
        js_str = str(js_data)
        js_str = js_str.replace('None','null')
        js_str = js_str.replace('\'','\"')
        return js_str

    def controller_thread_func(self):
        while True:
            out = self.controller_proc.stdout.readline()
            if out == '' and self.controller_proc.poll() != None:
                break
            if out != '':
                wx.CallAfter(self.controller.AppendText, out)

    def console_thread_func(self):
        while True:
            out = self.console_proc.stdout.readline()
            if out == '' and self.console_proc.poll() != None:
                break
            if out != '':
                wx.CallAfter(self.console.AppendText, out)


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