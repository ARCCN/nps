from config.config_constants import ALPHA_VALUE

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl

import wx
import wx.html2 as webview
import os
import json

def draw_graph(G, node_groups, edge_groups, leaves, node_map):
    mpl.rcParams['toolbar'] = 'None'
    mpl.rcParams['font.size'] = 11
    mpl.rcParams['font.family'] = 'Candara'

    pos = nx.spring_layout(G)

    fig = plt.figure(1, figsize=(15, 8))
    fig.canvas.set_window_title("Mininet CE Network Graph")
    fig.patch.set_facecolor('white')

    plt.subplot(121)
    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_visible(False)
    frame1.axes.get_yaxis().set_visible(False)
    frame1.patch.set_facecolor((1.0, 0.5, 1.0, 0.1))

    nx.draw_networkx_nodes(G, pos, node_size=50)
    nx.draw_networkx_edges(G, pos, alpha=ALPHA_VALUE, width=3.0)
    label_pos = {k: [v[0],v[1]+0.03] for k, v in pos.items()}
    nx.draw_networkx_labels(G, label_pos, font_size=10, font_family='candara')

    plt.subplot(122)
    frame2 = plt.gca()
    frame2.axes.get_xaxis().set_visible(False)
    frame2.axes.get_yaxis().set_visible(False)
    frame2.patch.set_facecolor((0.0, 0.0, 0.8, 0.1))

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

    label_pos = {k: [v[0],v[1]+0.03] for k, v in pos.items()}

    nx.draw_networkx_labels(G, label_pos, labels, font_size=10, font_family='candara')
    leg = plt.legend(pl_nodes, node_map.keys(), prop={'size': 8}, handletextpad=3)
    leg.legendPatch.set_alpha(0.77)

    plt.show()


########################################################################
class WebPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Based on the Webview demo in the wxPython demo"""
        wx.Panel.__init__(self, parent)


        self.current = os.path.realpath('GUI/GUI.html')
        self.frame = parent
        if parent:
            self.titleBase = parent.GetTitle()

        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.wv = webview.WebView.New(self)
        self.Bind(webview.EVT_WEB_VIEW_NAVIGATING, self.OnWebViewNavigating, self.wv)
        # self.Bind(webview.EVT_WEB_VIEW_LOADED, self.OnWebViewLoaded, self.wv)


        btn = wx.Button(self, -1, "Simulate", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnSimulateButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, -1, "Random", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnRandomButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        # btn = wx.Button(self, -1, "Open", style=wx.BU_EXACTFIT)
        # self.Bind(wx.EVT_BUTTON, self.OnOpenButton, btn)
        # btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
        #
        # btn = wx.Button(self, -1, "<--", style=wx.BU_EXACTFIT)
        # self.Bind(wx.EVT_BUTTON, self.OnPrevPageButton, btn)
        # btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
        # self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoBack, btn)
        #
        # btn = wx.Button(self, -1, "-->", style=wx.BU_EXACTFIT)
        # self.Bind(wx.EVT_BUTTON, self.OnNextPageButton, btn)
        # btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
        # self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoForward, btn)
        #
        # btn = wx.Button(self, -1, "Stop", style=wx.BU_EXACTFIT)
        # self.Bind(wx.EVT_BUTTON, self.OnStopButton, btn)
        # btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
        #
        # btn = wx.Button(self, -1, "Refresh", style=wx.BU_EXACTFIT)
        # self.Bind(wx.EVT_BUTTON, self.OnRefreshPageButton, btn)
        # btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)


        sizer.Add(btnSizer, 0, wx.EXPAND)
        sizer.Add(self.wv, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.wv.LoadURL(self.current)


    def ShutdownDemo(self):
        # put the frame title back
        if self.frame:
            self.frame.SetTitle(self.titleBase)


    # WebView events
    def OnWebViewNavigating(self, evt):
        # this event happens prior to trying to get a resource
        if evt.GetURL() == 'http://www.microsoft.com/':
            if wx.MessageBox("Are you sure you want to visit Microsoft?",
                             style=wx.YES_NO|wx.ICON_QUESTION) == wx.NO:
                # This is how you can cancel loading a page.
                evt.Veto()

    # def OnWebViewLoaded(self, evt):
    #     # The full document has loaded
    #     self.current = evt.GetURL()
    #     self.location.SetValue(self.current)


    # Control bar events
    # def OnLocationSelect(self, evt):
    #     url = self.location.GetStringSelection()
    #     self.wv.LoadURL(url)
    #
    # def OnLocationEnter(self, evt):
    #     url = self.location.GetValue()
    #     self.location.Append(url)
    #     self.wv.LoadURL(url)
    #
    #
    # def OnOpenButton(self, event):
    #     dlg = wx.TextEntryDialog(self, "Open Location",
    #                             "Enter a full URL or local path",
    #                             self.current, wx.OK|wx.CANCEL)
    #     dlg.CentreOnParent()
    #
    #     if dlg.ShowModal() == wx.ID_OK:
    #         self.current = dlg.GetValue()
    #         self.wv.LoadURL(self.current)
    #
    #     dlg.Destroy()

    def OnSimulateButton(self, event):
        prev_title = self.wv.GetCurrentTitle()
        self.wv.RunScript("document.title = document.cookie")
        cookies = self.wv.GetCurrentTitle()
        self.wv.RunScript("document.title = %s" % prev_title)
        graph_data = json.loads(cookies.split('=')[1])
        p = self.GetParent()
        p.set_graph_data(graph_data)

    def OnRandomButton(self, event):
        p = self.GetParent()
        p.set_random_flag(True)



    # def OnPrevPageButton(self, event):
    #     self.wv.GoBack()
    #
    # def OnNextPageButton(self, event):
    #     self.wv.GoForward()
    #
    # def OnCheckCanGoBack(self, event):
    #     event.Enable(self.wv.CanGoBack())
    #
    # def OnCheckCanGoForward(self, event):
    #     event.Enable(self.wv.CanGoForward())
    #
    # def OnStopButton(self, evt):
    #     self.wv.Stop()
    #
    # def OnRefreshPageButton(self, evt):
    #     self.wv.Reload()

########################################################################
class GUI_Editor(wx.Frame):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
        self.parent = parent
        """Constructor"""
        # wx.Frame.__init__(self, None, title="Mininet CE Graph Editor")
        wx.Frame.__init__(self, None, -1, 'Mininet CE Graph Editor', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.SetSize((875,675))

        panel = WebPanel(self)
        self.Show()

    def set_graph_data(self, data):
        self.parent.set_graph_data(data)
        self.Destroy()

    def set_random_flag(self, flag):
        self.parent.set_random_flag(flag)
        self.Destroy()


class GEdit():
    def __init__(self):
        self.graph_data = {}
        self.node_num_map = {}
        self.random_flag = False

    def main_loop(self):
        app = wx.App(False)
        frame = GUI_Editor(self)
        app.MainLoop()

    def set_graph_data(self, data):
        self.graph_data = data

    def set_random_flag(self, flag):
        self.random_flag = flag

    def get_random_flag(self):
        return self.random_flag

    def get_networkX_graph(self):
        G = nx.Graph()
        node_counter = 0
        for edge in self.graph_data['edges']:
            if edge[0] not in self.node_num_map.keys():
                G.add_node(node_counter)
                self.node_num_map[edge[0]] = node_counter
                node_counter += 1
            if edge[1] not in self.node_num_map.keys():
                G.add_node(node_counter)
                self.node_num_map[edge[1]] = node_counter
                node_counter += 1
            G.add_edge(self.node_num_map[edge[0]], self.node_num_map[edge[1]])
        return G

    def delete_gedit(self):
        self.Destroy()


if __name__ == "__main__":
    gui = GEdit()
    gui.main_loop()
    G = gui.get_networkX_graph()
    print G.nodes()
    print G.edges()