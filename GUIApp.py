from config.config_constants import ALPHA_VALUE, RESULT_PIC_DPI, CONTROLLER_PATH
from src.KThread             import KThread

import networkx          as nx
import matplotlib.pyplot as plt
import matplotlib        as mpl
import wx.html2          as webview

import pexpect
import sys
import subprocess
import wx
import os



def draw_graph(G, node_groups, edge_groups, leaves, node_map, pos):
    '''Drawing result graph to the file "result.png".

    Args:
        G: NetworkX graph.
        node_groups: Group ID to node-list map.
        edge_groups: Group ID to edge-list map.
        leaves: List of leave-nodes in network graph.
        node_map: Cluster node map.
        pos: Position of nodes in drawing graph.
    '''
    mpl.rcParams['toolbar'] = 'None'
    mpl.rcParams['font.size'] = 11
    mpl.rcParams['font.family'] = 'Candara'

    max_pos = 0
    for v in pos.values():
        if v[0] > max_pos:
            max_pos = v[0]
        if v[1] > max_pos:
            max_pos = v[1]
    avr_pos = max_pos / 50

    fig = plt.figure(1, figsize=(15, 8), frameon=False)
    fig.canvas.set_window_title("Mininet CE Network Graph")

    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(False)
    frame.patch.set_facecolor((0.0, 0.0, 0.8, 0.1))

    label_pos = {k: [v[0],v[1]+ avr_pos] for k, v in pos.items()}

    colors = ['b','g','r','c','m','y']

    labels = {}
    for n in G.nodes():
        if n in leaves:
            labels[n] = 'h' + str(n)
        else:
            labels[n] = 's' + str(n)

    pl_nodes = []
    for group in node_groups.keys():
        pl_node = nx.draw_networkx_nodes(G, pos, nodelist=node_groups[group], node_color=colors[group], node_size=50)
        pl_nodes.append(pl_node)

    for group in edge_groups.keys():
        if group != 'no_group':
            nx.draw_networkx_edges(G, pos, edgelist=edge_groups[group], edge_color=colors[group], alpha=ALPHA_VALUE, width=3.0)
        else:
            nx.draw_networkx_edges(G, pos, edgelist=edge_groups[group], edge_color='k', alpha=ALPHA_VALUE, width=3.0)

    nx.draw_networkx_labels(G, label_pos, labels, font_size=10, font_family='candara')
    leg = plt.legend(pl_nodes, node_map.keys(), prop={'size': 8}, handletextpad=3)
    leg.legendPatch.set_alpha(0.77)

    plt.savefig('GUI/result.png', dpi=RESULT_PIC_DPI, transparent=True, bbox_inches='tight', pad_inches=0)


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


        btn = CustomButton(self, -1, "Simulate")
        # btn.SetBackgroundColour('#93FF8C')
        self.Bind(wx.EVT_BUTTON, self.OnSimulateButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.RIGHT, 1)

        btn = CustomButton(self, -1, "Random")
        self.Bind(wx.EVT_BUTTON, self.OnRandomButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL)

        self.node_num = CustomTextCtrl(self, size=(117, -1))
        self.node_num.ChangeValue(str(17))
        btnSizer.Add(self.node_num, 0, wx.EXPAND|wx.ALL)

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
        self.wv.LoadURL(self.current)

    def onKeyPress(self, event):
        keycode = event.GetKeyCode()
        if keycode == 13: # ENTER KEY
            self.onSendButton(event)
        event.Skip()

    def onSendButton(self, event):
        cmd = self.cmd_line.GetValue()
        if cmd != 'exit':
            self.p.sendline(cmd)
            self.p.expect('mininet CE> ')
            for s in self.p.before:
                if len(s) != 0 and s != '\n':
                    self.console.AppendText(s)
            self.cmd_line.ChangeValue('')
        else:
            self.p.sendline(cmd)
            self.p.expect(pexpect.EOF)
            for s in self.p.before:
                if len(s) != 0 and s != '\n':
                    self.console.AppendText(s)
            self.cmd_line.ChangeValue('')
            self.controller_thread.kill()
            self.controller_proc.terminate()

    def OnSimulateButton(self, event):
        os.system("cp GUI/res/not_ready.png GUI/result.png")
        self.console.ChangeValue('')
        self.controller.ChangeValue('')
        prev_title = self.wv.GetCurrentTitle()
        self.wv.RunScript("document.title = document.cookie")
        cookies = self.wv.GetCurrentTitle()
        self.wv.RunScript("document.title = %s" % prev_title)
        graph_data = cookies.split('=')[1]
        # p = self.GetParent()
        # p.set_graph_data(graph_data)

        controller_cmd = "java -jar " + CONTROLLER_PATH + "/target/floodlight.jar"
        self.controller_proc = subprocess.Popen(controller_cmd, stdout=subprocess.PIPE, shell=True)
        self.controller_thread = KThread(target=self.controller_thread_func)
        self.controller_thread.setDaemon(True)
        self.controller_thread.start()

        self.p = pexpect.spawn(sys.prefix + '/bin/python main.py \'' + graph_data + '\'')

        self.p.expect('mininet CE> ')
        # self.p.expect(pexpect.EOF)
        for s in self.p.before:
            if len(s) != 0 and s != '\n':
                self.console.AppendText(s)

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
            self.wv.RunScript("document.cookie = 'graph=' + my_graph_editor.export_sage()")
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

class CustomButton(wx.Button):
    def __init__(self, *a, **k):
        style = ( wx.NO_BORDER )
        wx.Button.__init__(self, style=style, *a, **k)

        self.SetBackgroundColour('#EFE3FC')
        # more customization here

class CustomTextCtrl_readonly(wx.TextCtrl):
    def __init__(self, *a, **k):
        style = ( wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL )
        wx.TextCtrl.__init__(self, style=style, *a, **k)

        self.SetBackgroundColour('white')
        # more customization here

class CustomTextCtrl(wx.TextCtrl):
    def __init__(self, *a, **k):
        style = ( wx.NO_BORDER )
        wx.TextCtrl.__init__(self, style=style, *a, **k)

        self.SetBackgroundColour('white')
        # more customization here

class GUI_Editor(wx.Frame):
    """Class of GUI Editor.

    TODO
    """
    def __init__(self, parent):
        '''Cunstructor of GUI Editor.

        Args:
            parent:

        '''
        self.parent = parent
        style = ( wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.STAY_ON_TOP |  wx.NO_BORDER |
                      wx.FRAME_NO_TASKBAR | wx.CLIP_CHILDREN )
        """Constructor"""
        wx.Frame.__init__(self, None, -1, 'Mininet CE Graph Editor', style=style, pos=wx.Point(0, 50))
        self.SetSize((self.parent.width,self.parent.height)) # (1075,675)
        self.SetBackgroundColour('#CCCCFF')
        self.SetTransparent(230)

        panel = WebPanel(self)

        self.Show()


class GUIApp():
    '''Class of GUI Application.

    TODO
    '''
    def __init__(self, html_path, width=1075, height=655):
        '''Cunstructor of GUI Application.

        Args:
            html_path:
            width:
            height:
        '''
        os.system("cp GUI/res/not_ready.png GUI/result.png")

        self.graph_data = {}
        self.node_num_map = {}
        self.random_flag = False
        self.html_path = html_path
        self.width, self.height = width, height

    def main_loop(self):
        app = wx.App(False)
        frame = GUI_Editor(self)
        app.MainLoop()

    def get_networkX_graph(self):
        G = nx.Graph()
        node_counter = 0
        pos = {}
        for edge in self.graph_data['edges']:
            if edge[0] not in self.node_num_map.keys():
                G.add_node(node_counter)
                self.node_num_map[edge[0]] = node_counter
                pos[node_counter] = [self.graph_data['pos'][edge[0]][0], self.graph_data['pos'][edge[0]][1]]
                node_counter += 1
            if edge[1] not in self.node_num_map.keys():
                G.add_node(node_counter)
                self.node_num_map[edge[1]] = node_counter
                pos[node_counter] = [self.graph_data['pos'][edge[1]][0], self.graph_data['pos'][edge[1]][1]]
                node_counter += 1
            G.add_edge(self.node_num_map[edge[0]], self.node_num_map[edge[1]])
        return G, pos

    def delete_gedit(self):
        self.Destroy()


if __name__ == "__main__":
    gui = GUIApp()
    gui.main_loop()
    G = gui.get_networkX_graph()
    print G.nodes()
    print G.edges()