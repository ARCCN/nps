STRING_ALIGNMENT = 50
PYTHONPATH = '/Library/Frameworks/Python.framework/Versions/2.7/bin/python'

NPS_PATH = '/Users/vitalyantonenko/PycharmProjects/NPS'
CONTROLLER_PATH = '/Users/vitalyantonenko/Documents/ARCCN/Controllers/floodlight-0.90'
MALWARE_CENTER_PATH = '/Users/vitalyantonenko/PycharmProjects/NPS/src/malwaretools'
GUI_HTML = 'GUI/GUI.html'


LOG_FILEPATH      = NPS_PATH + '/logs/MininetCluster.log'
ROOT_LOG_FILEPATH = NPS_PATH + '/logs/MininetCluster_root.log'
MALWARE_LOG_PATH  = NPS_PATH + '/logs/MalwarePropagation.log'
SRC_SCRIPT_FOLDER = NPS_PATH + '/scripts/'
DST_SCRIPT_FOLDER = '/home/clusternode/MininetScripts/'
NODELIST_FILEPATH = NPS_PATH + '/config/nodelist.txt'
MAIN_DB_PATH      = NPS_PATH + '/tmp/'



MALWARE_MODE_ON = True
MALWARE_CENTER_IP   = '10.30.40.90'
MALWARE_CENTER_PORT = 56565
INFECTED_HOSTS_FILENAME = 'infected_hosts.db'

MAIN_DB_NAME = 'infected_hosts.db'


FIRST_HOST_IP = '1.2.3.1'

CLUSTER_NODE_MACHINE_NAME = 'clusternode-Parallels-Virtual-Platform'

MALWARE_PROP_DELAY             = 0
MALWARE_INIT_INF_PROB          = 5
MININET_SEGMENT_CREATION_DELAY = 0
MALWARE_PROP_STEP_NUMBER = 101

# MININETCE SIMULATION MODES CONSTANTS
MALWARE_PROPAGATION_MODE = False
CLI_MODE                 = True


HOST_NETMASK = 16 # mask of host intf on mininet cluster node
LINK_DELAY = 5 # default link delay in ms

ALPHA_VALUE = 0.33

RANDOM_GRAPH_FLAG = False
SEPARATE_GUI_FLAG = True
LOAD_GRAPH_FLAG = False
GRAPH_EDITOR_FLAG = False
DRAWING_FLAG = True
RANDOM_GRAPH_SIZE = 11

SCRIPT_FOLDER = 'scripts/nodes/'
REMOTE_CONTROLLER_IP   = '10.30.40.90'
REMOTE_CONTROLLER_PORT = '6633'


# CLI_PROMPT_STRING = 'mininet CE> '
CLI_PROMPT_STRING = ''

VIEW_PROGRAMM_NAME = 'Preview'

RESULT_PIC_DPI = 300

CHECK_PING_TIME_PERIOD = 30

