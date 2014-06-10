import cmd
import os

from src.clustertools.cluster_mininet_cmd_manager import send_mininet_ping_to_cluster_node, \
                                                         send_mininet_cmd_to_cluster_node
from config.config_constants                      import CLI_PROMPT_STRING, DST_SCRIPT_FOLDER, INFECTED_HOSTS_FILENAME

class CLI_director(cmd.Cmd):
    '''Class of CLI Director.

    TODO
    '''
    def __init__(self, hosts, nodes, cluster_info):
        '''Cunstructor of CLI Director.

        Args:
            host_map: Host IP to host name map.
            host_to_node_map: Host IP to node ID map.
            host_IP_map: Host name to host IP map.
            switch_num: Number of switches (not leave-nodes) in network graph.
            h_and_sw_node_map:
        '''
        cmd.Cmd.__init__(self)
        self.prompt = CLI_PROMPT_STRING
        self.intro  = "Welcome to NPS console!"  ## defaults to None
        self.hosts = hosts
        self.nodes = nodes
        self.cluster_info = cluster_info

    ## Command definitions ##
    def do_hist(self, args):
        """Print a list of commands that have been entered"""
        print self._hist

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    ## Command definitions to support Cmd object functionality ##
    def do_EOF(self, args):
        """Exit on system end of file character"""
        return self.do_exit(args)

    def do_shell(self, args):
        """Pass command to a system shell when line begins with '!'"""
        os.system(args)

    def do_help(self, args):
        """Get help on commands
           'help' or '?' with no arguments prints a list of commands for which help is available
           'help <command>' or '? <command>' gives help on <command>
        """
        ## The only reason to define this method is for the help text in the doc string
        cmd.Cmd.do_help(self, args)

    def is_host_exist(self, h):
        if self.is_hostname(h):
            if h not in self.hosts.keys():
                return None
            else:
                return h
        else:
            # FIX me when you have time
            find_flag = False
            for host in self.hosts.values():
                if host['IP'] == h:
                    find_flag = True
                    h = host['name']
                    break
            if find_flag:
                return h
            else:
                return None
            # FIX block end

    def do_ping(self, args):
        """Simple ping command"""
        args = args.split()
        if len(args) != 2:
            print('*** invalid number of arguments')
            return
        src = args[0]
        dst = args[1]
        src = self.is_host_exist(src)
        dst = self.is_host_exist(dst)
        if src == None:
            print('No such src host')
            return
        if dst == None:
            print('No such dst host')
            return
        dst_host = self.hosts[dst]
        cmd = src + ' ping -c 4 ' + dst_host['IP']
        src_host = self.hosts[src]
        node = self.nodes[src_host['nodeIP']]
        send_mininet_ping_to_cluster_node(node, cmd)

    def help_ping(self):
        print('usage:')
        print('\t_srcHostIP (_srcHostname) ping _dstHostIP (_dstHostname)')
        print('example:')
        print('\t10.0.0.1 ping 10.0.0.2')
        print('\th1       ping 10.0.0.2')
        print('\t10.0.0.1 ping h2')
        print('\th1       ping h2')

    def do_pingAll(self, args):
        #for src in self.host_IP_map.keys():
        #    for dst in self.host_IP_map.keys():
        #        if src != dst:
        #            dst = self.host_IP_map[dst]
        #            cmd = src + ' ping -c 4 ' + dst
        #            node = self.nodes[self.host_to_node_map[self.host_IP_map[src]]]
        #            send_mininet_ping_to_cluster_node(node, cmd)
        pass

    def help_pingAll(self):
        print('usage:')
        print('\tpingAll')
        print('example:')
        print('\tpingAll')

    def do_ifconfig(self, args):
        args = args.split()
        if len(args) != 1:
            print('*** invalid number of arguments')
            return
        src = args[0]

        src = self.is_host_exist(src)
        if src == None:
            print('No such src host')
            return
        cmd = src + ' ifconfig'
        src_host = self.hosts[src]
        node = self.nodes[src_host['nodeIP']]
        send_mininet_cmd_to_cluster_node(node, cmd, quite=False)

    def help_ifconfig(self):
        print('usage:')
        print('\t_srcHostIP (_srcHostname) ifconfig')
        print('example:')
        print('\t10.0.0.1 ifconfig')
        print('\th1       ifconfig')

    def do_hosts(self, args):
        args = args.split()
        if len(args) == 0:
            for host in self.hosts.values():
                print(host['name']),
                print(' '),
            print('')
        elif len(args) == 1 and args[0].lower() == 'ip':
            print('hostname'.center(7, ' ')),
            print(': '),
            print('host IP'.center(15, ' ')),
            print(' : ')
            for host in self.hosts.values():
                print(host['name'].ljust(7, ' ')),
                print(' : '),
                print(host['IP'])
        elif len(args) == 1 and args[0].lower() in ['node', 'cluster']:
            print('host IP'.center(15, ' ')),
            print(': '),
            print('node IP'.center(15, ' '))
            for host in self.hosts.values():
                print(host['IP'].ljust(15, ' ')),
                print(' : '),
                print(host['nodeIP'])
        elif len(args) == 1 and args[0].lower() == 'info':
            print('hostname'.center(7, ' ')),
            print(': '),
            print('host IP'.center(15, ' ')),
            print(' : '),
            print('node IP'.center(15, ' '))
            for host in self.hosts.values():
                print(host['name'].ljust(7, ' ')),
                print(' : '),
                print(host['IP'].ljust(15, ' ')),
                print(' : '),
                print(host['nodeIP'])
        else:
            print('wrong syntax in command "hosts"')

    def help_hosts(self):
        print('usage:')
        print('\thosts [ip, node, cluster, info]')
        print('example:')
        print('\thosts')
        print('\thosts ip')
        print('\thosts node')
        print('\thosts cluster')
        print('\thosts info')

    def do_hostnum(self,args):
        print('Number of hosts is ' + str(len(self.hosts)) + '.')

    def help_hostnum(self):
        print('usage:')
        print('\thostnum')

    def do_switchnum(self,args):
        print('Number of switches is ' + str(self.cluster_info['switch_number']) + '.')

    def help_switchnum(self):
        print('usage:')
        print('\tswitchnum')

    def do_setupsniffers(self, args):
        for host in self.hosts.values():
            cmd = host['name'] + ' python ' + DST_SCRIPT_FOLDER + 'port_sniffer.py ' + host['name'] + \
                  '-eth0 ' + DST_SCRIPT_FOLDER + INFECTED_HOSTS_FILENAME + ' &'
            #print cmd

            #print(self.nodes)
            node = self.nodes[host['nodeIP']]
            send_mininet_cmd_to_cluster_node(node, cmd, quite=True)
        print('Finish setuping sniffers!')

    def help_setupsniffers(self):
        print('usage:')
        print('\tsetupsniffers')


    def do_startworm(self, args):
        malware_hosts = args.split()

        for malware_host_name in malware_hosts:
            if self.is_hostname(malware_host_name):
                cmd = malware_host_name + ' python ' + DST_SCRIPT_FOLDER + 'worm_instance.py '\
                      + malware_host_name + '-eth0' + ' &'
                #print cmd
                host = self.hosts[malware_host_name]
                node = self.nodes[host['nodeIP']]
                send_mininet_cmd_to_cluster_node(node, cmd, quite=False)

    def help_startworm(self):
        print('usage:')
        print('\tstartworm hostname')

    def do_clusterinfo(self,args):
        print('Number of nodes in graph is ' + str(len(self.hosts.keys())+self.cluster_info['switch_number']) + '.')
        print('Number of hosts is ' + str(len(self.hosts.keys())) + '.')
        print('Number of switches is ' + str(self.cluster_info['switch_number']) + '.')
        print('')
        print('Cluster graph distribution:')
        for id, cn in self.cluster_info['node_info'].items():
            print('\t' + str(id) + ') ' + 'hosts = ' + str(cn[0]).rjust(5, ' ') + " ; "
                  + 'switches = ' + str(cn[1]).rjust(5, ' ') + ".")

    def help_clusterinfo(self):
        print('usage:')
        print('\tclusterinfo')

    ## Override methods in Cmd object ##
    def preloop(self):
        """Initialization before prompting user for commands.
           Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}

    def postloop(self):
        """Take care of any unfinished business.
           Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
        """
        cmd.Cmd.postloop(self)   ## Clean up command completion
        print "Exiting..."

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
        """
        self._hist += [line.strip()]
        return line

    def postcmd(self, stop, line):
        """If you want to stop the console, return something that evaluates to true.
           If you want to do some post command processing, do it here.
        """
        return stop

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        words = line.split()
        if len(words) == 3:
            if words[1] == 'ping':
                new_line = words[0] + ' ' + words[2]
                self.do_ping(new_line)
                return
        if len(words) == 2:
            if words[1] == 'ifconfig':
                new_line = words[0]
                self.do_ifconfig(new_line)
                return

        src_host = self.is_host_exist(words[0])
        if src_host == None:
            print('No such src host')
            return
        cmd = ''
        for word in words:
            cmd += word + ' '
        host = self.hosts[src_host]
        node = self.nodes[host['nodeIP']]
        send_mininet_cmd_to_cluster_node(node, cmd, quite=False)
        return

    def is_hostname(self, str):
        if str[0] == 'h':
            return True
        else:
            return False
