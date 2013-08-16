import cmd

from cluster_mininet_cmd_manager import send_mininet_ping_to_cluster_node, send_mininet_cmd_to_cluster_node
from config.config_constants import CLI_PROMPT_STRING

class CLI_director(cmd.Cmd):

    def __init__(self, host_map, host_to_node_map, host_IP_map, ssh_chan_map, switch_num, h_and_sw_node_map):
        cmd.Cmd.__init__(self)
        self.prompt = CLI_PROMPT_STRING
        self.intro  = "Welcome to Mininet CE console!"  ## defaults to None

        self.host_map = host_map
        self.host_to_node_map = host_to_node_map
        self.host_IP_map = host_IP_map
        self.ssh_chan_map = ssh_chan_map
        self.switch_num = switch_num
        self.h_and_sw_node_map = h_and_sw_node_map

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

    def do_ping(self, args):
        args = args.split()
        if len(args) != 2:
            print('*** invalid number of arguments')
            return
        src = args[0]
        dst = args[1]

        if src not in self.host_IP_map.keys() and src not in self.host_IP_map.values():
            print('No such src host')
            return
        if dst not in self.host_IP_map.keys() and dst not in self.host_IP_map.values():
            print('No such dst host')
            return

        if not self.is_hostname(src):
            src = self.host_map[src]
        if self.is_hostname(dst):
            dst = self.host_IP_map[dst]

        cmd = src + ' ping -c 4 ' + dst
        send_mininet_ping_to_cluster_node(self.host_to_node_map[self.host_IP_map[src]], cmd, self.ssh_chan_map)

    def help_ping(self):
        print('usage:')
        print('\t_srcHostIP (_srcHostname) ping _dstHostIP (_dstHostname)')
        print('example:')
        print('\t10.0.0.1 ping 10.0.0.2')
        print('\th1       ping 10.0.0.2')
        print('\t10.0.0.1 ping h2')
        print('\th1       ping h2')

    def do_pingAll(self, args):
        for src in self.host_IP_map.keys():
            for dst in self.host_IP_map.keys():
                if src != dst:
                    dst = self.host_IP_map[dst]
                    cmd = src + ' ping -c 4 ' + dst
                    send_mininet_ping_to_cluster_node(self.host_to_node_map[self.host_IP_map[src]], cmd, self.ssh_chan_map)

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

        if src not in self.host_IP_map.keys() and src not in self.host_IP_map.values():
            print('No such host')
            return

        if self.is_hostname(src):
            cmd = src + ' ifconfig'
        else:
            cmd = self.host_map[src] + ' ifconfig'
        if self.is_hostname(src):
            send_mininet_cmd_to_cluster_node(self.host_to_node_map[self.host_IP_map[src]], cmd,
                                             self.ssh_chan_map, quite=False)
        else:
            send_mininet_cmd_to_cluster_node(self.host_to_node_map[src], cmd, self.ssh_chan_map, quite=False)

    def help_ifconfig(self):
        print('usage:')
        print('\t_srcHostIP (_srcHostname) ifconfig')
        print('example:')
        print('\t10.0.0.1 ifconfig')
        print('\th1       ifconfig')

    def do_hosts(self, args):
        args = args.split()
        if len(args) == 0:
            for host in self.host_IP_map.keys():
                print(host),
                print(' '),
            print('')
        elif len(args) == 1 and args[0].lower() == 'ip':
            print('hostname'.center(7, ' ')),
            print(': '),
            print('host IP'.center(15, ' ')),
            print(' : ')
            for host, ip in self.host_IP_map.items():
                print(host.ljust(7, ' ')),
                print(' : '),
                print(ip)
        elif len(args) == 1 and args[0].lower() in ['node', 'cluster']:
            print('host IP'.center(15, ' ')),
            print(': '),
            print('node IP'.center(15, ' '))
            for host, node in self.host_to_node_map.items():
                print(host.ljust(15, ' ')),
                print(' : '),
                print(node)
        elif len(args) == 1 and args[0].lower() == 'info':
            print('hostname'.center(7, ' ')),
            print(': '),
            print('host IP'.center(15, ' ')),
            print(' : '),
            print('node IP'.center(15, ' '))
            for host, ip in self.host_IP_map.items():
                print(host.ljust(7, ' ')),
                print(' : '),
                print(ip.ljust(15, ' ')),
                print(' : '),
                print(self.host_to_node_map[ip])
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
        print('Number of hosts is ' + str(len(self.host_map.keys())) + '.')

    def help_hostnum(self):
        print('usage:')
        print('\thostnum')

    def do_switchnum(self,args):
        print('Number of switches is ' + str(self.switch_num) + '.')

    def help_switchnum(self):
        print('usage:')
        print('\tswitchnum')

    def do_clusterinfo(self,args):
        print('Number of nodes in graph is ' + str(len(self.host_map.keys())+self.switch_num) + '.')
        print('Number of hosts is ' + str(len(self.host_map.keys())) + '.')
        print('Number of switches is ' + str(self.switch_num) + '.')
        print('')
        print('Cluster graph distribution:')
        for cn in self.h_and_sw_node_map.keys():
            print('\t' + str(cn) + ') ' + 'hosts = ' + str(self.h_and_sw_node_map[cn][0]).rjust(5, ' ') + " ; "
                  + 'switches = ' + str(self.h_and_sw_node_map[cn][1]).rjust(5, ' ') + ".")

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
        self._hist += [ line.strip() ]
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
        if self.is_hostname(words[0]):
            cmd = ''
            for word in words:
                cmd += word + ' '
            send_mininet_cmd_to_cluster_node(self.host_to_node_map[self.host_IP_map[words[0]]],
                                              cmd, self.ssh_chan_map, quite=False)
            return
        else:
            print('Sorry, unknown command')

            # try:
            #     exec(line) in self._locals, self._globals
            # except Exception, e:
            #     print e.__class__, ":", e

    def is_hostname(self, str):
        if str[0] == 'h':
            return True
        else:
            return False
