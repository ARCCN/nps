import subprocess
import time
import wx
from config.config_constants import NODELIST_FILEPATH, CHECK_PING_TIME_PERIOD
from src.KThread import KThread

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


class NodeStatusPanel(wx.Panel):
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

        self.node_map = self.read_nodelist_from_file(NODELIST_FILEPATH)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.node_labels = []
        for node in self.node_map.keys():
            #response = os.system("ping -c 1 " + node)
            node_label = wx.StaticText(self, -1, node, style=wx.ALIGN_CENTER)
            #if response == 0:
            #    node_label.SetForegroundColour('green')
            #else:
            #    node_label.SetForegroundColour('red')
            hbox.Add(node_label, 1, wx.EXPAND|wx.RIGHT, 1)
            self.node_labels.append(node_label)

        self.SetSizer(hbox)

        self.ping_thread = KThread(target=self.ping_thread_func)
        self.ping_thread.setDaemon(True)
        self.ping_thread.start()

    def ping_thread_func(self):
        while True:
            for node_label in self.node_labels:
                ping = subprocess.Popen(["ping", "-c", "1", node_label.GetLabel()], stdout=subprocess.PIPE, shell=False)
                ping.wait()
                if ping.returncode != 0:
                    node_label.SetForegroundColour('red')
                else:
                    node_label.SetForegroundColour('green')
            time.sleep(CHECK_PING_TIME_PERIOD)


    def read_nodelist_from_file(self, nodelist_filepath):
        '''Read list of cluster nodes from file.

        Args:
            nodelist_file: Name of file with list of cluster nodes.
        '''
        node_map = {}
        # open nodelist file
        #logger_MininetCE.info('Reading nodelist from file')
        nodelist_file = open(nodelist_filepath, 'r')
        file_lines = nodelist_file.readlines()
        for file_line in file_lines:
            splitted_line = file_line.split(' ')
            node_map[splitted_line[0]]             = splitted_line[2]
        return node_map