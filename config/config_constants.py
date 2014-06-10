
### FILE PATHS
## GENERAL PATHS
PYTHONPATH = '/Library/Frameworks/Python.framework/Versions/2.7/bin/python'
NPS_PATH = '/Users/vitalyantonenko/PycharmProjects/NPS'
CONTROLLER_PATH = '/Users/vitalyantonenko/Documents/ARCCN/Controllers/floodlight-0.90'
MALWARE_CENTER_PATH = '/Users/vitalyantonenko/PycharmProjects/NPS/src/malwaretools'
GUI_HTML = 'GUI/GUI.html'
## SCRIPT PATHS
SRC_SCRIPT_FOLDER = NPS_PATH + '/scripts/'
DST_SCRIPT_FOLDER = '/home/clusternode/MininetScripts/'
## CONFIG PATHS
NODELIST_FILEPATH = NPS_PATH + '/config/nodelist.txt'
MAIN_DB_PATH      = NPS_PATH + '/tmp/'

### MALWARE MODE
MALWARE_MODE_ON = True
MALWARE_CENTER_IP   = 'localhost'
MALWARE_CENTER_PORT = 56565
INFECTED_HOSTS_FILENAME = 'infected_hosts.db'
#MAIN_DB_NAME = 'infected_hosts.db'

### HOSTS CONFIG
FIRST_HOST_IP = '1.2.3.1'
HOST_NETMASK = 16 # mask of host intf on mininet cluster node
LINK_DELAY = 5 # default link delay in ms
NO_DELAY_FLAG = True

### CLUSTER NODE CONFIG
CLUSTER_NODE_MACHINE_NAME = 'clusternode-Parallels-Virtual-Platform'

### MININETCE SIMULATION MODES CONSTANTS
CLI_MODE = True

### APPIRANCE CONFIG
STRING_ALIGNMENT = 50
ALPHA_VALUE = 0.33
CLI_PROMPT_STRING = ''
VIEW_PROGRAMM_NAME = 'Preview'
RESULT_PIC_DPI = 300

### GENERAL CONFIG
DRAWING_FLAG = True
SCRIPT_FOLDER = 'scripts/nodes/'
CHECK_PING_TIME_PERIOD = 30

### CONTROLLER CONFIG
REMOTE_CONTROLLER_IP   = 'localhost'
REMOTE_CONTROLLER_PORT = '6633'



