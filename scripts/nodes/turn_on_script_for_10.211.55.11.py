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
        s0 = self.addSwitch( 's0' )
        s1 = self.addSwitch( 's1' )
        s3 = self.addSwitch( 's3' )
        s4 = self.addSwitch( 's4' )
        s5 = self.addSwitch( 's5' )
        s7 = self.addSwitch( 's7' )
        s8 = self.addSwitch( 's8' )
        s9 = self.addSwitch( 's9' )
        h11 = self.addHost( 'h11', ip='1.2.3.1/16' )
        s12 = self.addSwitch( 's12' )
        s13 = self.addSwitch( 's13' )
        s14 = self.addSwitch( 's14' )
        s16 = self.addSwitch( 's16' )
        s18 = self.addSwitch( 's18' )
        h20 = self.addHost( 'h20', ip='1.2.3.2/16' )
        s21 = self.addSwitch( 's21' )
        s22 = self.addSwitch( 's22' )
        h23 = self.addHost( 'h23', ip='1.2.3.3/16' )
        s24 = self.addSwitch( 's24' )
        s25 = self.addSwitch( 's25' )
        s27 = self.addSwitch( 's27' )
        s28 = self.addSwitch( 's28' )
        h29 = self.addHost( 'h29', ip='1.2.3.4/16' )
        h30 = self.addHost( 'h30', ip='1.2.3.5/16' )
        h31 = self.addHost( 'h31', ip='1.2.3.6/16' )
        s34 = self.addSwitch( 's34' )
        s37 = self.addSwitch( 's37' )
        s39 = self.addSwitch( 's39' )
        s40 = self.addSwitch( 's40' )
        s41 = self.addSwitch( 's41' )
        h42 = self.addHost( 'h42', ip='1.2.3.7/16' )
        s43 = self.addSwitch( 's43' )
        h44 = self.addHost( 'h44', ip='1.2.3.8/16' )
        s45 = self.addSwitch( 's45' )
        s46 = self.addSwitch( 's46' )
        h49 = self.addHost( 'h49', ip='1.2.3.9/16' )
        s50 = self.addSwitch( 's50' )
        s51 = self.addSwitch( 's51' )
        s52 = self.addSwitch( 's52' )
        h53 = self.addHost( 'h53', ip='1.2.3.10/16' )
        h54 = self.addHost( 'h54', ip='1.2.3.11/16' )
        s55 = self.addSwitch( 's55' )
        h57 = self.addHost( 'h57', ip='1.2.3.12/16' )
        s58 = self.addSwitch( 's58' )
        s59 = self.addSwitch( 's59' )
        h60 = self.addHost( 'h60', ip='1.2.3.13/16' )
        h61 = self.addHost( 'h61', ip='1.2.3.14/16' )
        h62 = self.addHost( 'h62', ip='1.2.3.15/16' )
        s63 = self.addSwitch( 's63' )
        h64 = self.addHost( 'h64', ip='1.2.3.16/16' )
        h65 = self.addHost( 'h65', ip='1.2.3.17/16' )
        s66 = self.addSwitch( 's66' )
        h68 = self.addHost( 'h68', ip='1.2.3.18/16' )
        h69 = self.addHost( 'h69', ip='1.2.3.19/16' )
        h70 = self.addHost( 'h70', ip='1.2.3.20/16' )
        h72 = self.addHost( 'h72', ip='1.2.3.21/16' )
        s74 = self.addSwitch( 's74' )
        h76 = self.addHost( 'h76', ip='1.2.3.22/16' )
        h77 = self.addHost( 'h77', ip='1.2.3.23/16' )
        s78 = self.addSwitch( 's78' )
        h79 = self.addHost( 'h79', ip='1.2.3.24/16' )
        h80 = self.addHost( 'h80', ip='1.2.3.25/16' )
        h82 = self.addHost( 'h82', ip='1.2.3.26/16' )
        h83 = self.addHost( 'h83', ip='1.2.3.27/16' )
        s84 = self.addSwitch( 's84' )
        h86 = self.addHost( 'h86', ip='1.2.3.28/16' )
        s87 = self.addSwitch( 's87' )
        h89 = self.addHost( 'h89', ip='1.2.3.29/16' )
        h92 = self.addHost( 'h92', ip='1.2.3.30/16' )
        s94 = self.addSwitch( 's94' )
        h95 = self.addHost( 'h95', ip='1.2.3.31/16' )
        s97 = self.addSwitch( 's97' )
        h99 = self.addHost( 'h99', ip='1.2.3.32/16' )
        h100 = self.addHost( 'h100', ip='1.2.3.33/16' )
        h101 = self.addHost( 'h101', ip='1.2.3.34/16' )
        h102 = self.addHost( 'h102', ip='1.2.3.35/16' )
        h103 = self.addHost( 'h103', ip='1.2.3.36/16' )
        h104 = self.addHost( 'h104', ip='1.2.3.37/16' )
        h105 = self.addHost( 'h105', ip='1.2.3.38/16' )
        s106 = self.addSwitch( 's106' )
        h107 = self.addHost( 'h107', ip='1.2.3.39/16' )
        h108 = self.addHost( 'h108', ip='1.2.3.40/16' )
        s109 = self.addSwitch( 's109' )
        h110 = self.addHost( 'h110', ip='1.2.3.41/16' )
        h111 = self.addHost( 'h111', ip='1.2.3.42/16' )
        s112 = self.addSwitch( 's112' )
        h113 = self.addHost( 'h113', ip='1.2.3.43/16' )
        h114 = self.addHost( 'h114', ip='1.2.3.44/16' )
        h115 = self.addHost( 'h115', ip='1.2.3.45/16' )
        h116 = self.addHost( 'h116', ip='1.2.3.46/16' )
        h117 = self.addHost( 'h117', ip='1.2.3.47/16' )
        h119 = self.addHost( 'h119', ip='1.2.3.48/16' )
        h120 = self.addHost( 'h120', ip='1.2.3.49/16' )
        h121 = self.addHost( 'h121', ip='1.2.3.50/16' )
        s124 = self.addSwitch( 's124' )
        s125 = self.addSwitch( 's125' )
        s126 = self.addSwitch( 's126' )
        h127 = self.addHost( 'h127', ip='1.2.3.51/16' )
        h128 = self.addHost( 'h128', ip='1.2.3.52/16' )
        h130 = self.addHost( 'h130', ip='1.2.3.53/16' )
        h131 = self.addHost( 'h131', ip='1.2.3.54/16' )
        h134 = self.addHost( 'h134', ip='1.2.3.55/16' )
        h135 = self.addHost( 'h135', ip='1.2.3.56/16' )
        h137 = self.addHost( 'h137', ip='1.2.3.57/16' )
        h138 = self.addHost( 'h138', ip='1.2.3.58/16' )
        h139 = self.addHost( 'h139', ip='1.2.3.59/16' )
        h140 = self.addHost( 'h140', ip='1.2.3.60/16' )
        s141 = self.addSwitch( 's141' )
        h142 = self.addHost( 'h142', ip='1.2.3.61/16' )
        h144 = self.addHost( 'h144', ip='1.2.3.62/16' )
        h145 = self.addHost( 'h145', ip='1.2.3.63/16' )
        h147 = self.addHost( 'h147', ip='1.2.3.64/16' )
        h148 = self.addHost( 'h148', ip='1.2.3.65/16' )
        h149 = self.addHost( 'h149', ip='1.2.3.66/16' )
        h150 = self.addHost( 'h150', ip='1.2.3.67/16' )
        h151 = self.addHost( 'h151', ip='1.2.3.68/16' )
        h154 = self.addHost( 'h154', ip='1.2.3.69/16' )
        h156 = self.addHost( 'h156', ip='1.2.3.70/16' )
        h157 = self.addHost( 'h157', ip='1.2.3.71/16' )
        h158 = self.addHost( 'h158', ip='1.2.3.72/16' )
        h159 = self.addHost( 'h159', ip='1.2.3.73/16' )
        h160 = self.addHost( 'h160', ip='1.2.3.74/16' )
        h162 = self.addHost( 'h162', ip='1.2.3.75/16' )
        h163 = self.addHost( 'h163', ip='1.2.3.76/16' )
        h164 = self.addHost( 'h164', ip='1.2.3.77/16' )
        h166 = self.addHost( 'h166', ip='1.2.3.78/16' )
        h167 = self.addHost( 'h167', ip='1.2.3.79/16' )
        h168 = self.addHost( 'h168', ip='1.2.3.80/16' )
        h169 = self.addHost( 'h169', ip='1.2.3.81/16' )
        h170 = self.addHost( 'h170', ip='1.2.3.82/16' )
        h172 = self.addHost( 'h172', ip='1.2.3.83/16' )
        h173 = self.addHost( 'h173', ip='1.2.3.84/16' )
        h174 = self.addHost( 'h174', ip='1.2.3.85/16' )
        h175 = self.addHost( 'h175', ip='1.2.3.86/16' )
        h176 = self.addHost( 'h176', ip='1.2.3.87/16' )

        "Add links"
        self.addLink( s0, s1, delay='5ms')
        self.addLink( s0, s4, delay='5ms')
        self.addLink( s0, s5, delay='5ms')
        self.addLink( s0, s12, delay='5ms')
        self.addLink( s0, h77, delay='5ms')
        self.addLink( s0, h116, delay='5ms')
        self.addLink( s0, h89, delay='5ms')
        self.addLink( s0, h119, delay='5ms')
        self.addLink( s0, h20, delay='5ms')
        self.addLink( s0, h31, delay='5ms')
        self.addLink( s0, s94, delay='5ms')
        self.addLink( s0, h159, delay='5ms')
        self.addLink( s1, h130, delay='5ms')
        self.addLink( s1, s3, delay='5ms')
        self.addLink( s1, h29, delay='5ms')
        self.addLink( s1, h113, delay='5ms')
        self.addLink( s1, s24, delay='5ms')
        self.addLink( s1, h61, delay='5ms')
        self.addLink( s3, s34, delay='5ms')
        self.addLink( s3, s58, delay='5ms')
        self.addLink( s4, h131, delay='5ms')
        self.addLink( s4, h104, delay='5ms')
        self.addLink( s4, h44, delay='5ms')
        self.addLink( s4, h11, delay='5ms')
        self.addLink( s4, h172, delay='5ms')
        self.addLink( s4, h121, delay='5ms')
        self.addLink( s5, s7, delay='5ms')
        self.addLink( s5, s8, delay='5ms')
        self.addLink( s5, s9, delay='5ms')
        self.addLink( s5, h107, delay='5ms')
        self.addLink( s5, s22, delay='5ms')
        self.addLink( s5, h103, delay='5ms')
        self.addLink( s5, h127, delay='5ms')
        self.addLink( s7, s40, delay='5ms')
        self.addLink( s7, h54, delay='5ms')
        self.addLink( s8, h128, delay='5ms')
        self.addLink( s8, h174, delay='5ms')
        self.addLink( s8, s45, delay='5ms')
        self.addLink( s9, h102, delay='5ms')
        self.addLink( s9, h42, delay='5ms')
        self.addLink( s9, h145, delay='5ms')
        self.addLink( s9, h151, delay='5ms')
        self.addLink( s9, s124, delay='5ms')
        self.addLink( s9, h101, delay='5ms')
        self.addLink( s12, s51, delay='5ms')
        self.addLink( s12, h162, delay='5ms')
        self.addLink( s12, h99, delay='5ms')
        self.addLink( s12, h134, delay='5ms')
        self.addLink( s12, s13, delay='5ms')
        self.addLink( s12, s14, delay='5ms')
        self.addLink( s12, s16, delay='5ms')
        self.addLink( s12, s27, delay='5ms')
        self.addLink( s12, h83, delay='5ms')
        self.addLink( s12, s52, delay='5ms')
        self.addLink( s12, h149, delay='5ms')
        self.addLink( s12, h86, delay='5ms')
        self.addLink( s12, h154, delay='5ms')
        self.addLink( s12, s59, delay='5ms')
        self.addLink( s12, h92, delay='5ms')
        self.addLink( s13, h173, delay='5ms')
        self.addLink( s13, h79, delay='5ms')
        self.addLink( s13, h144, delay='5ms')
        self.addLink( s13, s18, delay='5ms')
        self.addLink( s13, s21, delay='5ms')
        self.addLink( s13, h23, delay='5ms')
        self.addLink( s13, h30, delay='5ms')
        self.addLink( s14, h108, delay='5ms')
        self.addLink( s16, h120, delay='5ms')
        self.addLink( s16, s25, delay='5ms')
        self.addLink( s16, h60, delay='5ms')
        self.addLink( s18, h64, delay='5ms')
        self.addLink( s18, s41, delay='5ms')
        self.addLink( s18, s106, delay='5ms')
        self.addLink( s18, s78, delay='5ms')
        self.addLink( s18, h142, delay='5ms')
        self.addLink( s21, s39, delay='5ms')
        self.addLink( s22, s28, delay='5ms')
        self.addLink( s22, h138, delay='5ms')
        self.addLink( s22, h68, delay='5ms')
        self.addLink( s22, h69, delay='5ms')
        self.addLink( s24, s66, delay='5ms')
        self.addLink( s24, h163, delay='5ms')
        self.addLink( s24, h70, delay='5ms')
        self.addLink( s24, h169, delay='5ms')
        self.addLink( s24, s43, delay='5ms')
        self.addLink( s24, h140, delay='5ms')
        self.addLink( s24, s84, delay='5ms')
        self.addLink( s25, h65, delay='5ms')
        self.addLink( s25, h164, delay='5ms')
        self.addLink( s27, h139, delay='5ms')
        self.addLink( s28, s37, delay='5ms')
        self.addLink( s34, h168, delay='5ms')
        self.addLink( s34, h158, delay='5ms')
        self.addLink( s37, h148, delay='5ms')
        self.addLink( s39, h160, delay='5ms')
        self.addLink( s40, s74, delay='5ms')
        self.addLink( s41, s97, delay='5ms')
        self.addLink( s43, s46, delay='5ms')
        self.addLink( s43, h49, delay='5ms')
        self.addLink( s43, h115, delay='5ms')
        self.addLink( s43, s55, delay='5ms')
        self.addLink( s43, h157, delay='5ms')
        self.addLink( s43, h62, delay='5ms')
        self.addLink( s45, h72, delay='5ms')
        self.addLink( s46, h80, delay='5ms')
        self.addLink( s46, s50, delay='5ms')
        self.addLink( s46, h76, delay='5ms')
        self.addLink( s50, s63, delay='5ms')
        self.addLink( s51, h111, delay='5ms')
        self.addLink( s52, h53, delay='5ms')
        self.addLink( s55, h100, delay='5ms')
        self.addLink( s55, h167, delay='5ms')
        self.addLink( s55, h82, delay='5ms')
        self.addLink( s55, h57, delay='5ms')
        self.addLink( s55, s125, delay='5ms')
        self.addLink( s58, h150, delay='5ms')
        self.addLink( s58, h166, delay='5ms')
        self.addLink( s59, s126, delay='5ms')
        self.addLink( s63, s112, delay='5ms')
        self.addLink( s66, h110, delay='5ms')
        self.addLink( s74, h156, delay='5ms')
        self.addLink( s78, s87, delay='5ms')
        self.addLink( s78, h135, delay='5ms')
        self.addLink( s84, h114, delay='5ms')
        self.addLink( s87, h95, delay='5ms')
        self.addLink( s94, s109, delay='5ms')
        self.addLink( s97, h105, delay='5ms')
        self.addLink( s106, h117, delay='5ms')
        self.addLink( s109, h175, delay='5ms')
        self.addLink( s112, h176, delay='5ms')
        self.addLink( s124, h137, delay='5ms')
        self.addLink( s125, s141, delay='5ms')
        self.addLink( s126, h147, delay='5ms')
        self.addLink( s141, h170, delay='5ms')


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
        mn.add_preconf_service( 'h100', 2 , 'dhcp' )
        mn.add_preconf_service( 'h101', 2 , 'dhcp' )
        mn.add_preconf_service( 'h102', 2 , 'dhcp' )
        mn.add_preconf_service( 'h103', 2 , 'dhcp' )
        mn.add_preconf_service( 'h104', 2 , 'dhcp' )
        mn.add_preconf_service( 'h105', 2 , 'dhcp' )
        mn.add_preconf_service( 'h107', 2 , 'dhcp' )
        mn.add_preconf_service( 'h108', 2 , 'dhcp' )
        mn.add_preconf_service( 'h11', 2 , 'dhcp' )
        mn.add_preconf_service( 'h110', 2 , 'dhcp' )
        mn.add_preconf_service( 'h111', 2 , 'dhcp' )
        mn.add_preconf_service( 'h113', 2 , 'dhcp' )
        mn.add_preconf_service( 'h114', 2 , 'dhcp' )
        mn.add_preconf_service( 'h115', 2 , 'dhcp' )
        mn.add_preconf_service( 'h116', 2 , 'dhcp' )
        mn.add_preconf_service( 'h117', 2 , 'dhcp' )
        mn.add_preconf_service( 'h119', 2 , 'dhcp' )
        mn.add_preconf_service( 'h120', 2 , 'dhcp' )
        mn.add_preconf_service( 'h121', 2 , 'dhcp' )
        mn.add_preconf_service( 'h127', 2 , 'dhcp' )
        mn.add_preconf_service( 'h128', 2 , 'dhcp' )
        mn.add_preconf_service( 'h130', 2 , 'dhcp' )
        mn.add_preconf_service( 'h131', 2 , 'dhcp' )
        mn.add_preconf_service( 'h134', 2 , 'dhcp' )
        mn.add_preconf_service( 'h135', 2 , 'dhcp' )
        mn.add_preconf_service( 'h137', 2 , 'dhcp' )
        mn.add_preconf_service( 'h138', 2 , 'dhcp' )
        mn.add_preconf_service( 'h139', 2 , 'dhcp' )
        mn.add_preconf_service( 'h140', 2 , 'dhcp' )
        mn.add_preconf_service( 'h142', 2 , 'dhcp' )
        mn.add_preconf_service( 'h144', 2 , 'dhcp' )
        mn.add_preconf_service( 'h145', 2 , 'dhcp' )
        mn.add_preconf_service( 'h147', 2 , 'dhcp' )
        mn.add_preconf_service( 'h148', 2 , 'dhcp' )
        mn.add_preconf_service( 'h149', 2 , 'dhcp' )
        mn.add_preconf_service( 'h150', 2 , 'dhcp' )
        mn.add_preconf_service( 'h151', 2 , 'dhcp' )
        mn.add_preconf_service( 'h154', 2 , 'dhcp' )
        mn.add_preconf_service( 'h156', 2 , 'dhcp' )
        mn.add_preconf_service( 'h157', 2 , 'dhcp' )
        mn.add_preconf_service( 'h158', 2 , 'dhcp' )
        mn.add_preconf_service( 'h159', 2 , 'dhcp' )
        mn.add_preconf_service( 'h160', 2 , 'dhcp' )
        mn.add_preconf_service( 'h162', 2 , 'dhcp' )
        mn.add_preconf_service( 'h163', 2 , 'dhcp' )
        mn.add_preconf_service( 'h164', 2 , 'dhcp' )
        mn.add_preconf_service( 'h166', 2 , 'dhcp' )
        mn.add_preconf_service( 'h167', 2 , 'dhcp' )
        mn.add_preconf_service( 'h168', 2 , 'dhcp' )
        mn.add_preconf_service( 'h169', 2 , 'dhcp' )
        mn.add_preconf_service( 'h170', 2 , 'dhcp' )
        mn.add_preconf_service( 'h172', 2 , 'dhcp' )
        mn.add_preconf_service( 'h173', 2 , 'dhcp' )
        mn.add_preconf_service( 'h174', 2 , 'dhcp' )
        mn.add_preconf_service( 'h175', 2 , 'dhcp' )
        mn.add_preconf_service( 'h176', 2 , 'dhcp' )
        mn.add_preconf_service( 'h20', 2 , 'dhcp' )
        mn.add_preconf_service( 'h23', 2 , 'dhcp' )
        mn.add_preconf_service( 'h29', 2 , 'dhcp' )
        mn.add_preconf_service( 'h30', 2 , 'dhcp' )
        mn.add_preconf_service( 'h31', 2 , 'dhcp' )
        mn.add_preconf_service( 'h42', 2 , 'dhcp' )
        mn.add_preconf_service( 'h44', 2 , 'dhcp' )
        mn.add_preconf_service( 'h49', 2 , 'dhcp' )
        mn.add_preconf_service( 'h53', 2 , 'dhcp' )
        mn.add_preconf_service( 'h54', 2 , 'dhcp' )
        mn.add_preconf_service( 'h57', 2 , 'dhcp' )
        mn.add_preconf_service( 'h60', 2 , 'dhcp' )
        mn.add_preconf_service( 'h61', 2 , 'dhcp' )
        mn.add_preconf_service( 'h62', 2 , 'dhcp' )
        mn.add_preconf_service( 'h64', 2 , 'dhcp' )
        mn.add_preconf_service( 'h65', 2 , 'dhcp' )
        mn.add_preconf_service( 'h68', 2 , 'dhcp' )
        mn.add_preconf_service( 'h69', 2 , 'dhcp' )
        mn.add_preconf_service( 'h70', 2 , 'dhcp' )
        mn.add_preconf_service( 'h72', 2 , 'dhcp' )
        mn.add_preconf_service( 'h76', 2 , 'dhcp' )
        mn.add_preconf_service( 'h77', 2 , 'dhcp' )
        mn.add_preconf_service( 'h79', 2 , 'dhcp' )
        mn.add_preconf_service( 'h80', 2 , 'dhcp' )
        mn.add_preconf_service( 'h82', 2 , 'dhcp' )
        mn.add_preconf_service( 'h83', 2 , 'dhcp' )
        mn.add_preconf_service( 'h86', 2 , 'dhcp' )
        mn.add_preconf_service( 'h89', 2 , 'dhcp' )
        mn.add_preconf_service( 'h92', 2 , 'dhcp' )
        mn.add_preconf_service( 'h95', 2 , 'dhcp' )
        mn.add_preconf_service( 'h99', 2 , 'dhcp' )
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
