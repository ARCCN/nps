import cmd

from cluster_mininet_cmd_manager import send_mininet_ping_to_cluster_node

class CLI_director(cmd.Cmd):

    def __init__(self, host_map, host_to_node_map, ssh_chan_map):
        cmd.Cmd.__init__(self)
        self.prompt = "+> "
        self.intro  = "Welcome to Mininet CE console!"  ## defaults to None

        self.host_map = host_map
        self.host_to_node_map = host_to_node_map
        self.ssh_chan_map = ssh_chan_map

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
        src_ip = args[0]
        dst_ip = args[1]

        cmd = self.host_map[src_ip] + ' ping -c 4 ' + dst_ip
        send_mininet_ping_to_cluster_node(self.host_to_node_map[src_ip], cmd, self.ssh_chan_map)

    def help_ping(self):
        print('usage:')
        print('\t_srcHostIP ping _dstHostIP')
        print('example:')
        print('\t10.0.0.1 ping 10.0.0.2')


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
        if words[1] == 'ping' and len(words) == 3:
            new_line = words[0] + ' ' + words[2]
            self.do_ping(new_line)
        else:
            try:
                exec(line) in self._locals, self._globals
            except Exception, e:
                print e.__class__, ":", e