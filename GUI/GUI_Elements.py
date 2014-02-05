import subprocess
import time
import wx
from config.config_constants import NODELIST_FILEPATH, CHECK_PING_TIME_PERIOD, MALWARE_MODE_ON
from src.KThread import KThread
from src.mininettools.mininet_script_operator import define_leaves_in_graph

import json
import networkx as nx

__author__ = 'vitalyantonenko'


class CustomButton(wx.Button):
    def __init__(self, *a, **k):
        style = ( wx.NO_BORDER )
        wx.Button.__init__(self,  style=style, *a, **k)

        self.SetBackgroundColour('#B2B2B2') #C4C4FF
        # more customization here

class CustomToggleButton(wx.ToggleButton):
    def __init__(self, *a, **k):
        #style = ( wx.NO_BORDER )
        #wx.ToggleButton.__init__(self,  style=style, *a, **k)
        wx.ToggleButton.__init__(self, *a, **k)

        self.SetBackgroundColour('#B2B2B2') #C4C4FF
        # more customization here


class CustomTextCtrl_readonly(wx.TextCtrl):
    def __init__(self, *a, **k):
        style = ( wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL )
        wx.TextCtrl.__init__(self, style=style, *a, **k)

        self.SetBackgroundColour('#D8D8D8')
        self.SetMaxLength(100)
        # more customization here


class CustomTextCtrl(wx.TextCtrl):
    def __init__(self, *a, **k):
        style = ( wx.NO_BORDER | wx.TE_CENTRE )
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

        label = wx.StaticText(self, -1, 'Cluster nodes status:')
        hbox.Add(label, 0, wx.EXPAND|wx.RIGHT, 1)


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
                    node_label.SetBackgroundColour('#F79C94')
                else:
                    node_label.SetBackgroundColour('#A3F291')
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

class GraphEditorPanel(wx.Panel):
    """
    """
    #----------------------------------------------------------------------
    def __init__(self, parent, wv, inf_hosts_list=None):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             ) #size=(235,100)

        self.tabs = {'Result', 'Visualizer', 'WorldMap'}

        self.wv = wv
        if MALWARE_MODE_ON:
            self.inf_hosts_list = inf_hosts_list
            self. graph_data = ""

        self.current_tab = 'Editor'
        self.options_status = False

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.live_btn = CustomButton(self, -1, "Live")
        # btn.SetBackgroundColour('#93FF8C') B2B2B2
        self.Bind(wx.EVT_BUTTON, self.OnLiveButton, self.live_btn)
        hbox.Add(self.live_btn, 1, wx.EXPAND|wx.RIGHT, 1)

        self.options_btn = CustomButton(self, -1, "Options")
        # btn.SetBackgroundColour('#93FF8C') B2B2B2
        self.Bind(wx.EVT_BUTTON, self.OnOptionsButton, self.options_btn)
        hbox.Add(self.options_btn, 1, wx.EXPAND|wx.RIGHT, 1)

        if MALWARE_MODE_ON:
            self.showinf_btn = CustomButton(self, -1, "Show Inf")
            # btn.SetBackgroundColour('#93FF8C') B2B2B2
            self.Bind(wx.EVT_BUTTON, self.OnShowInfButton, self.showinf_btn)
            self.showinf_btn.Hide()
            hbox.Add(self.showinf_btn, 1, wx.EXPAND|wx.RIGHT, 1)

            self.showinf_chb = wx.CheckBox(self, label='Show Inf')
            self.showinf_chb.Bind(wx.EVT_CHECKBOX, self.OnShowInfChbClick)
            hbox.Add(self.showinf_chb, 1, wx.EXPAND|wx.RIGHT, 1)
            self.showinf_chb.Enable(False)
            self.update_thread = KThread(target=self.update_thread_func)
            self.update_thread.setDaemon(True)
            self.thread_already_created = True

        self.editor_btn = CustomButton(self, -1, "Editor")
        #self.editor_btn.SetBackgroundColour('#FFFFFF')
        self.Bind(wx.EVT_BUTTON, self.OnEditorButton, self.editor_btn)
        hbox.Add(self.editor_btn, 1, wx.EXPAND|wx.RIGHT, 1)

        self.result_btn = CustomButton(self, -1, "Result")
        # btn.SetBackgroundColour('#93FF8C') B2B2B2
        self.Bind(wx.EVT_BUTTON, self.OnResultButton, self.result_btn)
        hbox.Add(self.result_btn, 1, wx.EXPAND|wx.RIGHT, 1)

        self.visualiser_btn = CustomButton(self, -1, "Visualiser")
        # btn.SetBackgroundColour('#93FF8C') B2B2B2
        self.Bind(wx.EVT_BUTTON, self.OnVisualiserButton, self.visualiser_btn)
        hbox.Add(self.visualiser_btn, 1, wx.EXPAND|wx.RIGHT, 1)

        self.worldmap_btn = CustomButton(self, -1, "World Map")
        # btn.SetBackgroundColour('#93FF8C') B2B2B2
        self.Bind(wx.EVT_BUTTON, self.OnWorldMapButton, self.worldmap_btn)
        hbox.Add(self.worldmap_btn, 1, wx.EXPAND|wx.RIGHT, 1)

        btn = CustomButton(self, -1, "Undo")
        # btn.SetBackgroundColour('#93FF8C') B2B2B2
        self.Bind(wx.EVT_BUTTON, self.OnUndoButton, btn)
        hbox.Add(btn, 1, wx.EXPAND|wx.RIGHT, 1)

        btn = CustomButton(self, -1, "Reset")
        # btn.SetBackgroundColour('#93FF8C') B2B2B2
        self.Bind(wx.EVT_BUTTON, self.OnResetButton, btn)
        hbox.Add(btn, 1, wx.EXPAND|wx.RIGHT, 1)

        btn = CustomButton(self, -1, "Help")
        # btn.SetBackgroundColour('#93FF8C') B2B2B2
        self.Bind(wx.EVT_BUTTON, self.OnHelpButton, btn)
        hbox.Add(btn, 1, wx.EXPAND|wx.RIGHT, 1)

        self.SetSizer(hbox)


    def show_options(self):
        self.wv.RunScript("$('#graph_ed').animate({'width': my_graph_editor.get_SIZE_x() + 185 + 'px'}, "
                              "{queue: true, duration: 'fast', easing: 'linear', complete: function (){ "
                              " $('#graph_ed' + ' #graph_editor_tweaks').slideToggle('fast'); "
                              "     my_graph_editor.set_UIside_panel_opened(true);}});")
        self.wv.RunScript("$('#graph_ed' + ' #tweaks_button').toggleClass('graph_editor_button_on');")
        self.options_status = True
        #self.options_btn.SetBackgroundColour('#FFFFFF')

    def hide_options(self):
        self.wv.RunScript("$('#graph_ed' + ' #graph_editor_tweaks').slideToggle('fast', function ()"
                              " {$('#graph_ed').animate({'width': my_graph_editor.get_SIZE_x() +'px'},"
                              " {queue: true, duration: 'fast', easing: 'linear'}); "
                              "     my_graph_editor.set_UIside_panel_opened(false);});")
        self.wv.RunScript("$('#graph_ed' + ' #tweaks_button').toggleClass('graph_editor_button_on');")
        self.options_status = False
        #self.options_btn.SetBackgroundColour('#B2B2B2')
        #self.editor_btn.SetBackgroundColour('#FFFFFF')

    def show_result(self):
        self.wv.RunScript("document.getElementById('result_image').src = \"result.png?random=\"+new Date().getTime();")
        self.wv.RunScript("$('#graph_ed' + ' #result').show();")
        self.wv.RunScript("canvas = $('#graph_ed' +' canvas')[0];")
        self.wv.RunScript("$(canvas).hide();")
        self.wv.RunScript("$('#graph_ed'+' #result_button').toggleClass('graph_editor_button_on');")
        self.current_tab = 'Result'
        #self.result_btn.SetBackgroundColour('#FFFFFF')
        #self.editor_btn.SetBackgroundColour('#B2B2B2')

    def hide_result(self):
        self.wv.RunScript("canvas = $('#graph_ed' +' canvas')[0];")
        self.wv.RunScript("$(canvas).show();")
        self.wv.RunScript("$('#graph_ed' + ' #result').hide();")
        self.wv.RunScript("$('#graph_ed' + ' #result_button').toggleClass('graph_editor_button_on');")
        self.current_tab = 'Editor'
        #self.result_btn.SetBackgroundColour('#B2B2B2')
        #self.editor_btn.SetBackgroundColour('#FFFFFF')

    def show_visualiser(self):
        self.wv.RunScript("$('#graph_ed' + ' #vizualizer').show();")
        self.wv.RunScript("canvas = $('#graph_ed' +' canvas')[0];")
        self.wv.RunScript("$(canvas).hide();")
        self.wv.RunScript("$('#graph_ed'+' #vizualizer_button').toggleClass('graph_editor_button_on');")
        self.current_tab = 'Visualiser'
        #self.visualiser_btn.SetBackgroundColour('#FFFFFF')
        #self.editor_btn.SetBackgroundColour('#B2B2B2')

    def hide_visualiser(self):
        self.wv.RunScript("canvas = $('#graph_ed' +' canvas')[0];")
        self.wv.RunScript("$(canvas).show();")
        self.wv.RunScript("$('#graph_ed' + ' #vizualizer').hide();")
        self.wv.RunScript("$('#graph_ed' +' #vizualizer_button').toggleClass('graph_editor_button_on');")
        self.current_tab = 'Editor'
        #self.visualiser_btn.SetBackgroundColour('#B2B2B2')
        #self.editor_btn.BackgroundColour('#FFFFFF')

    def show_worldmap(self):
        self.wv.RunScript("$('#graph_ed' + ' #worldmap').show();")
        self.wv.RunScript("$('#graph_ed' + ' #worldmap').fadeIn().resize();")
        self.wv.RunScript("canvas = $('#graph_ed' +' canvas')[0];")
        self.wv.RunScript("$(canvas).hide();")
        self.wv.RunScript("$('#graph_ed'+' #worldmap_button').toggleClass('graph_editor_button_on');")
        self.current_tab = 'WorldMap'
        #self.worldmap_btn.SetBackgroundColour('#FFFFFF')
        #self.editor_btn.SetBackgroundColour('#B2B2B2')

    def hide_worldmap(self):
        self.wv.RunScript("canvas = $('#graph_ed' +' canvas')[0];")
        self.wv.RunScript("$(canvas).show();")
        self.wv.RunScript("$('#graph_ed' + ' #worldmap').hide();")
        self.wv.RunScript("$('#graph_ed' +' #worldmap_button').toggleClass('graph_editor_button_on');")
        self.current_tab = 'Editor'
        #self.worldmap_btn.SetBackgroundColour('#B2B2B2')
        #self.editor_btn.SetBackgroundColour('#FFFFFF')

    def go_to_editor_tab(self):
        if self.current_tab == 'Editor' and self.options_status == True:
            self.hide_options()
        if self.current_tab == 'Result':
            self.hide_result()
        if self.current_tab == 'Visualiser':
            self.hide_visualiser()
        if self.current_tab == 'WorldMap':
            self.hide_worldmap()

    def set_graph_data(self, graph_data):
        self.graph_data = graph_data

    def enable_showinf_chb(self):
        self.showinf_chb.Enable(True)

    def change_hosts_color(self, graph_data):
        # Draw in green only leaves
        js = json.loads(graph_data)
        G = nx.Graph()
        for edge in js['edges']:
            if int(edge[0]) not in G.nodes():
                G.add_node(int(edge[0]))
            if int(edge[1]) not in G.nodes():
                G.add_node(int(edge[1]))
            G.add_edge(int(edge[0]), int(edge[1]))
        leaves = define_leaves_in_graph(G)
        for l in leaves:
            self.wv.RunScript("my_graph_editor.set_node_vulnerable(\"" + str(l) + "\");")


    def OnLiveButton(self, event):
        if self.current_tab == 'Editor':
            self.wv.RunScript("my_graph_editor.toggle_live();")

    def OnOptionsButton(self, event):
        if not self.options_status and self.current_tab == 'Editor':
            self.show_options()
        elif self.options_status and self.current_tab == 'Editor':
            self.hide_options()

    def OnShowInfButton(self, event):
        if self.current_tab == 'Editor':
            for host in self.inf_hosts_list:
                self.wv.RunScript("my_graph_editor.set_node_infected(\"" + host[1:] + "\")")

    def OnShowInfChbClick(self, event):
        sender = event.GetEventObject()
        isChecked = sender.GetValue()

        if isChecked:
            self.change_hosts_color(self.graph_data)
            if not self.thread_already_created:
                self.update_thread = KThread(target=self.update_thread_func)
                self.update_thread.setDaemon(True)
            self.update_thread.start()
        else:
            self.update_thread.kill()
            self.thread_already_created = False
            self.wv.RunScript("my_graph_editor.set_nodes_invulnerable()")

    def update_thread_func(self):
        while True:
            time.sleep(1)
            evt = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.showinf_btn.GetId())
            wx.PostEvent(self.showinf_btn, evt)

    def OnEditorButton(self, event):
        self.go_to_editor_tab()
        #self.editor_btn.SetBackgroundColour('#FFFFFF')



    def OnResultButton(self, event):
        if self.current_tab == 'Result':
            self.hide_result()
        else:
            self.go_to_editor_tab()
            self.show_result()

    def OnVisualiserButton(self, event):
        if self.current_tab == 'Visualiser':
            self.hide_visualiser()
        else:
            self.go_to_editor_tab()
            self.show_visualiser()

    def OnWorldMapButton(self, event):
        if self.current_tab == 'WorldMap':
            self.hide_worldmap()
        else:
            self.go_to_editor_tab()
            self.show_worldmap()

    def OnUndoButton(self, event):
        if self.current_tab == 'Editor':
            self.wv.RunScript("my_graph_editor.undo_remove();")

    def OnResetButton(self, event):
        if self.current_tab == 'Editor':
            self.wv.RunScript("my_graph_editor.erase_graph();")

    def OnHelpButton(self, event):
        self.wv.RunScript("$('#help_dialog').dialog('open');")


