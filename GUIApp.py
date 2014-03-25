import os

import networkx          as nx
import matplotlib.pyplot as plt
import matplotlib        as mpl
import wx

from GUI.GUI_WebPanel        import WebPanel
from config.config_constants import ALPHA_VALUE, RESULT_PIC_DPI
from config.config_colors import COLOR_NAMES

def draw_graph(G, groups, leaves, nodes, pos):
    '''Drawing result graph to the file "result.png".

    Args:

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

    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(False)
    frame.patch.set_facecolor((0.0, 0.0, 0.8, 0.1))

    label_pos = {k: [v[0],v[1]+ avr_pos] for k, v in pos.items()}

    #colors = ['b','g','r','c','m','y']
    colors = COLOR_NAMES.values()

    labels = {}
    for n in G.nodes():
        if n in leaves:
            labels[n] = 'h' + str(n)
        else:
            labels[n] = 's' + str(n)

    pl_nodes = []
    for id, group in groups.items():
        if id != 'no_group':
            pl_node = nx.draw_networkx_nodes(G, pos, nodelist=group['vertexes'], node_color=colors[id], node_size=50)
            pl_nodes.append(pl_node)
            nx.draw_networkx_edges(G, pos, edgelist=group['edges'], edge_color=colors[id],
                                   alpha=ALPHA_VALUE, width=3.0)
        else:
            nx.draw_networkx_edges(G, pos, edgelist=group['edges'], edge_color='k', alpha=ALPHA_VALUE, width=3.0)

    nx.draw_networkx_labels(G, label_pos, labels, font_size=10, font_family='candara')

    leg = plt.legend(pl_nodes, nodes.keys(), prop={'size': 8}, handletextpad=3)
    leg.legendPatch.set_alpha(0.77)
    plt.savefig('GUI/result.png', dpi=RESULT_PIC_DPI, transparent=True, bbox_inches='tight', pad_inches=0)


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
        style = (wx.DEFAULT_FRAME_STYLE) # wx.STAY_ON_TOP | wx.CLOSE_BOX | wx.FRAME_NO_TASKBAR | wx.SYSTEM_MENU | wx.CAPTION | wx.NO_BORDER | wx.CLIP_CHILDREN
        """Constructor"""
        wx.Frame.__init__(self, None, -1, 'NPS Graph Editor', style=style, pos=wx.Point(0, 50))
        self.SetSize((self.parent.width,self.parent.height)) # (1075,675)
        self.SetBackgroundColour('#CECECE') #CCCCFF
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