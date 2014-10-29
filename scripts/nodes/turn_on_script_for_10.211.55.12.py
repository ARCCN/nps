#!/usr/bin/env python


from optparse import OptionParser
import os
import sys
import time
import re

# Fix setuptools' evil madness, and open up (more?) security holes
if 'PYTHONPATH' in os.environ:
    sys.path = os.environ[ 'PYTHONPATH' ].split( ':' ) + sys.path

from mininet.clean import cleanup
from mininet.cli import CLI
from mininet.log import lg, LEVELS, info
from mininet.net import Mininet, MininetWithControlNet, VERSION
from mininet.node import ( Host, CPULimitedHost, Controller, OVSController,
                           NOX, RemoteController, UserSwitch, OVSKernelSwitch,
                           OVSLegacyKernelSwitch )
from mininet.link import Link, TCLink, Intf
from mininet.topo import Topo, SingleSwitchTopo, LinearTopo, SingleSwitchReversedTopo
from mininet.topolib import TreeTopo
from mininet.util import custom, customConstructor, quietRun
from mininet.util import buildTopo


sw_ext_intf = ['s0','s2']

class MyTopo( Topo ):
    "Auto generated topology for this Mininet Node"
    def __init__( self ):
        Topo.__init__( self )

        "Add hosts and swiches"
        s2 = self.addSwitch( 's2' )
        s6 = self.addSwitch( 's6' )
        s10 = self.addSwitch( 's10' )
        s15 = self.addSwitch( 's15' )
        s17 = self.addSwitch( 's17' )
        s19 = self.addSwitch( 's19' )
        s26 = self.addSwitch( 's26' )
        h32 = self.addHost( 'h32', ip='1.2.3.88/16' )
        s33 = self.addSwitch( 's33' )
        h35 = self.addHost( 'h35', ip='1.2.3.89/16' )
        s36 = self.addSwitch( 's36' )
        h38 = self.addHost( 'h38', ip='1.2.3.90/16' )
        h47 = self.addHost( 'h47', ip='1.2.3.91/16' )
        h48 = self.addHost( 'h48', ip='1.2.3.92/16' )
        s56 = self.addSwitch( 's56' )
        h67 = self.addHost( 'h67', ip='1.2.3.93/16' )
        h71 = self.addHost( 'h71', ip='1.2.3.94/16' )
        s73 = self.addSwitch( 's73' )
        s75 = self.addSwitch( 's75' )
        s81 = self.addSwitch( 's81' )
        s85 = self.addSwitch( 's85' )
        h88 = self.addHost( 'h88', ip='1.2.3.95/16' )
        h90 = self.addHost( 'h90', ip='1.2.3.96/16' )
        h91 = self.addHost( 'h91', ip='1.2.3.97/16' )
        h93 = self.addHost( 'h93', ip='1.2.3.98/16' )
        h96 = self.addHost( 'h96', ip='1.2.3.99/16' )
        h98 = self.addHost( 'h98', ip='1.2.3.100/16' )
        h118 = self.addHost( 'h118', ip='1.2.3.101/16' )
        h122 = self.addHost( 'h122', ip='1.2.3.102/16' )
        h123 = self.addHost( 'h123', ip='1.2.3.103/16' )
        h129 = self.addHost( 'h129', ip='1.2.3.104/16' )
        s132 = self.addSwitch( 's132' )
        s133 = self.addSwitch( 's133' )
        h136 = self.addHost( 'h136', ip='1.2.3.105/16' )
        h143 = self.addHost( 'h143', ip='1.2.3.106/16' )
        h146 = self.addHost( 'h146', ip='1.2.3.107/16' )
        h152 = self.addHost( 'h152', ip='1.2.3.108/16' )
        s153 = self.addSwitch( 's153' )
        h155 = self.addHost( 'h155', ip='1.2.3.109/16' )
        h161 = self.addHost( 'h161', ip='1.2.3.110/16' )
        h165 = self.addHost( 'h165', ip='1.2.3.111/16' )
        h171 = self.addHost( 'h171', ip='1.2.3.112/16' )

        "Add links"
        self.addLink( s2, h96, delay='5ms')
        self.addLink( s2, s6, delay='5ms')
        self.addLink( s2, h71, delay='5ms')
        self.addLink( s2, h136, delay='5ms')
        self.addLink( s2, h48, delay='5ms')
        self.addLink( s2, s17, delay='5ms')
        self.addLink( s2, s56, delay='5ms')
        self.addLink( s2, s26, delay='5ms')
        self.addLink( s2, h90, delay='5ms')
        self.addLink( s6, s10, delay='5ms')
        self.addLink( s6, s133, delay='5ms')
        self.addLink( s10, s36, delay='5ms')
        self.addLink( s10, s15, delay='5ms')
        self.addLink( s15, h93, delay='5ms')
        self.addLink( s17, s33, delay='5ms')
        self.addLink( s17, h38, delay='5ms')
        self.addLink( s17, s75, delay='5ms')
        self.addLink( s17, s19, delay='5ms')
        self.addLink( s17, h118, delay='5ms')
        self.addLink( s17, h91, delay='5ms')
        self.addLink( s19, h32, delay='5ms')
        self.addLink( s19, h35, delay='5ms')
        self.addLink( s19, h47, delay='5ms')
        self.addLink( s19, h143, delay='5ms')
        self.addLink( s26, s73, delay='5ms')
        self.addLink( s33, h152, delay='5ms')
        self.addLink( s33, h122, delay='5ms')
        self.addLink( s33, h67, delay='5ms')
        self.addLink( s36, h129, delay='5ms')
        self.addLink( s56, s85, delay='5ms')
        self.addLink( s73, h165, delay='5ms')
        self.addLink( s75, h88, delay='5ms')
        self.addLink( s75, h98, delay='5ms')
        self.addLink( s75, h123, delay='5ms')
        self.addLink( s75, s81, delay='5ms')
        self.addLink( s81, s132, delay='5ms')
        self.addLink( s85, h161, delay='5ms')
        self.addLink( s132, h146, delay='5ms')
        self.addLink( s132, h171, delay='5ms')
        self.addLink( s133, s153, delay='5ms')
        self.addLink( s153, h155, delay='5ms')


def checkIntf( intf ):
    "Make sure intf exists and is not configured."
    if ( ' %s:' % intf ) not in quietRun( 'ip link show' ):
        error( 'Error:', intf, 'does not exist!\n' )
        exit( 1 )
    ips = re.findall( r'\d+\.\d+\.\d+\.\d+', quietRun( 'ifconfig ' + intf ) )
    if ips:
        error( 'Error:', intf, 'has an IP address,'
                               'and is probably in use!\n' )
        exit( 1 )

#navy
import mininet.services

# built in topologies, created only when run
TOPODEF = 'minimal'
TOPOS = { 'minimal': lambda: SingleSwitchTopo( k=2 ),
          'linear': LinearTopo,
          'reversed': SingleSwitchReversedTopo,
          'single': SingleSwitchTopo,
          'tree': TreeTopo }

SWITCHDEF = 'ovsk'
SWITCHES = { 'user': UserSwitch,
             'ovsk': OVSKernelSwitch,
             'ovsl': OVSLegacyKernelSwitch }

HOSTDEF = 'proc'
HOSTS = { 'proc': Host,
          'rt': custom( CPULimitedHost, sched='rt' ),
          'cfs': custom( CPULimitedHost, sched='cfs' ) }

CONTROLLERDEF = 'ovsc'
CONTROLLERS = { 'ref': Controller,
                'ovsc': OVSController,
                'nox': NOX,
                'remote': RemoteController,
               'none': lambda name: None }

LINKDEF = 'default'
LINKS = { 'default': TCLink,
          'tc': TCLink }


# optional tests to run
TESTS = [ 'cli', 'build', 'pingall', 'pingpair', 'iperf', 'all', 'iperfudp',
            'none' ]

ALTSPELLING = { 'pingall': 'pingAll',
                'pingpair': 'pingPair',
                'iperfudp': 'iperfUdp',
                'iperfUDP': 'iperfUdp' }


def addDictOption( opts, choicesDict, default, name, helpStr=None ):
    """Convenience function to add choices dicts to OptionParser.
       opts: OptionParser instance
       choicesDict: dictionary of valid choices, must include default
       default: default choice key
       name: long option name
       help: string"""
    if default not in choicesDict:
        raise Exception( 'Invalid  default %s for choices dict: %s' %
                         ( default, name ) )
    if not helpStr:
        helpStr = ( '|'.join( sorted( choicesDict.keys() ) ) +
                    '[,param=value...]' )
    opts.add_option( '--' + name,
                     type='string',
                     default = default,
                     help = helpStr )


def version( *_args ):
    "Print Mininet version and exit"
    print "%s" % VERSION
    exit()

class MininetRunner( object ):
    "Build, setup, and run Mininet."

    def __init__( self ):
        "Init."
        self.options = None
        self.args = None  # May be used someday for more CLI scripts
        self.validate = None

        self.parseArgs()
        self.setup()
        self.begin()

    def setCustom( self, name, value ):
        "Set custom parameters for MininetRunner."
        if name in ( 'topos', 'switches', 'hosts', 'controllers' ):
            # Update dictionaries
            param = name.upper()
            globals()[ param ].update( value )
        elif name == 'validate':
            # Add custom validate function
            self.validate = value
        else:
            # Add or modify global variable or class
            globals()[ name ] = value

    def parseCustomFile( self, fileName ):
        "Parse custom file and add params before parsing cmd-line options."
        customs = {}
        if os.path.isfile( fileName ):
            execfile( fileName, customs, customs )
            for name, val in customs.iteritems():
                self.setCustom( name, val )
        else:
            raise Exception( 'could not find custom file: %s' % fileName )

    def parseArgs( self ):
        """Parse command-line args and return options object.
           returns: opts parse options dict"""
        if '--custom' in sys.argv:
            index = sys.argv.index( '--custom' )
            if len( sys.argv ) > index + 1:
                filename = sys.argv[ index + 1 ]
                self.parseCustomFile( filename )
            else:
                raise Exception( 'Custom file name not found' )

        desc = ( "The %prog utility creates Mininet network from the\n"
                 "command line. It can create parametrized topologies,\n"
                 "invoke the Mininet CLI, and run tests." )

        usage = ( '%prog [options]\n'
                  '(type %prog -h for details)' )

        opts = OptionParser( description=desc, usage=usage )
        addDictOption( opts, SWITCHES, SWITCHDEF, 'switch' )
        addDictOption( opts, HOSTS, HOSTDEF, 'host' )
        addDictOption( opts, CONTROLLERS, CONTROLLERDEF, 'controller' )
        addDictOption( opts, LINKS, LINKDEF, 'link' )
        addDictOption( opts, TOPOS, TOPODEF, 'topo' )

        opts.add_option( '--clean', '-c', action='store_true',
                         default=False, help='clean and exit' )
        opts.add_option( '--custom', type='string', default=None,
                         help='read custom topo and node params from .py' +
                         'file' )
        opts.add_option( '--test', type='choice', choices=TESTS,
                         default=TESTS[ 0 ],
                         help='|'.join( TESTS ) )
        opts.add_option( '--xterms', '-x', action='store_true',
                         default=False, help='spawn xterms for each node' )
        opts.add_option( '--ipbase', '-i', type='string', default='10.0.0.0/8',
                         help='base IP address for hosts' )
        opts.add_option( '--mac', action='store_true',
                         default=False, help='automatically set host MACs' )
        opts.add_option( '--arp', action='store_true',
                         default=False, help='set all-pairs ARP entries' )
        opts.add_option( '--verbosity', '-v', type='choice',
                         choices=LEVELS.keys(), default = 'info',
                         help = '|'.join( LEVELS.keys() )  )
        opts.add_option( '--innamespace', action='store_true',
                         default=False, help='sw and ctrl in namespace?' )
        opts.add_option( '--listenport', type='int', default=6634,
                         help='base port for passive switch listening' )
        opts.add_option( '--nolistenport', action='store_true',
                         default=False, help="don't use passive listening " +
                         "port")
        opts.add_option( '--pre', type='string', default=None,
                         help='CLI script to run before tests' )
        opts.add_option( '--post', type='string', default=None,
                         help='CLI script to run after tests' )
        opts.add_option( '--pin', action='store_true',
                         default=False, help="pin hosts to CPU cores "
                         "(requires --host cfs or --host rt)" )
        opts.add_option( '--version', action='callback', callback=version )

        self.options, self.args = opts.parse_args()

    def setup( self ):
        "Setup and validate environment."

        # set logging verbosity
        if LEVELS[self.options.verbosity] > LEVELS['output']:
            print ( '*** WARNING: selected verbosity level (%s) will hide CLI '
                    'output!\n'
                    'Please restart Mininet with -v [debug, info, output].'
                    % self.options.verbosity )
        lg.setLogLevel( self.options.verbosity )

    def begin( self ):
        "Create and run mininet."

        if self.options.clean:
            cleanup()
            exit()

        start = time.time()

#navy
        #topo = buildTopo( TOPOS, self.options.topo )
        topo = MyTopo()
        switch = customConstructor( SWITCHES, self.options.switch )
        host = customConstructor( HOSTS, self.options.host )
        controller = lambda name: RemoteController( name,ip='10.211.55.2',port=int('6633') )
        link = customConstructor( LINKS, self.options.link )

        if self.validate:
            self.validate( self.options )

        inNamespace = self.options.innamespace
        #navy
        #Net = MininetWithControlNet if inNamespace else Mininet
        Net = mininet.services.wrpMininet

        ipBase = self.options.ipbase
        xterms = self.options.xterms
        mac = self.options.mac
        arp = self.options.arp
        pin = self.options.pin
        listenPort = None
        if not self.options.nolistenport:
            listenPort = self.options.listenport


        intfName = 'eth1'
        info( '*** Checking', intfName, '\n' )
        checkIntf( intfName )

        mn = Net( topo=topo,
            switch=switch, host=host, controller=controller,
            link=link,
            ipBase=ipBase,
            inNamespace=inNamespace,
            xterms=xterms, autoSetMacs=mac,
            autoStaticArp=arp, autoPinCpus=pin,
#navy
#           listenPort=listenPort )
            listenPort=listenPort, services = True )


        for sw in mn.switches:
            if sw.name in sw_ext_intf:
                info( '*** Adding hardware interface', intfName, 'to switch',
                    sw.name, '\n' )
                _intf = Intf( intfName, node=sw )

        info( '*** Note: you may need to reconfigure the interfaces for '
            'the Mininet hosts:\n', mn.hosts, '\n' )

#navy
#Add services here
        mn.add_preconf_service( 'h118', 2 , 'dhcp' )
        mn.add_preconf_service( 'h122', 2 , 'dhcp' )
        mn.add_preconf_service( 'h123', 2 , 'dhcp' )
        mn.add_preconf_service( 'h129', 2 , 'dhcp' )
        mn.add_preconf_service( 'h136', 2 , 'dhcp' )
        mn.add_preconf_service( 'h143', 2 , 'dhcp' )
        mn.add_preconf_service( 'h146', 2 , 'dhcp' )
        mn.add_preconf_service( 'h152', 2 , 'dhcp' )
        mn.add_preconf_service( 'h155', 2 , 'dhcp' )
        mn.add_preconf_service( 'h161', 2 , 'dhcp' )
        mn.add_preconf_service( 'h165', 2 , 'dhcp' )
        mn.add_preconf_service( 'h171', 2 , 'dhcp' )
        mn.add_preconf_service( 'h32', 2 , 'dhcp' )
        mn.add_preconf_service( 'h35', 2 , 'dhcp' )
        mn.add_preconf_service( 'h38', 2 , 'dhcp' )
        mn.add_preconf_service( 'h47', 2 , 'dhcp' )
        mn.add_preconf_service( 'h48', 2 , 'dhcp' )
        mn.add_preconf_service( 'h67', 2 , 'dhcp' )
        mn.add_preconf_service( 'h71', 2 , 'dhcp' )
        mn.add_preconf_service( 'h88', 2 , 'dhcp' )
        mn.add_preconf_service( 'h90', 2 , 'dhcp' )
        mn.add_preconf_service( 'h91', 2 , 'dhcp' )
        mn.add_preconf_service( 'h93', 2 , 'dhcp' )
        mn.add_preconf_service( 'h96', 2 , 'dhcp' )
        mn.add_preconf_service( 'h98', 2 , 'dhcp' )
#-----------------


        if self.options.pre:
            CLI( mn, script=self.options.pre )

        test = self.options.test
        test = ALTSPELLING.get( test, test )

        mn.start()

        if test == 'none':
            pass
        elif test == 'all':
            mn.start()
            mn.ping()
            mn.iperf()
        elif test == 'cli':
            CLI( mn )
        elif test != 'build':
            getattr( mn, test )()

        if self.options.post:
            CLI( mn, script=self.options.post )

        mn.stop()

        elapsed = float( time.time() - start )
        info( 'completed in %0.3f seconds\n' % elapsed )


if __name__ == "__main__":
    MininetRunner()
