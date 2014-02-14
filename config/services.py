#!/usr/bin/env python

"""
Mininet example, based on mininet runner by Brandon Heller 
Creating mininet hosts, loaded with some network daemons (services)
in a regular manner.
"""

from optparse import OptionParser
import os
import sys
import time
import re

# Fix setuptools' evil madness, and open up (more?) security holes
if 'PYTHONPATH' in os.environ:
    sys.path = os.environ[ 'PYTHONPATH' ].split( ':' ) + sys.path

MN_CFGDIR = '/home/netapps'
MN_ETCDIR = 'etc'
MN_VARDIR = 'var'
MN_LOCKDIR = 'lock'
MN_RUNDIR  = 'run'

cfg_homepath = '/tmp' 
if 'HOME' is os.environ:
    cfg_homepath = os.environ['HOME']

MN_CFGPATH = os.path.join(cfg_homepath, MN_CFGDIR)
MN_ETCPATH = os.path.join(MN_CFGPATH, MN_ETCDIR)
MN_VARPATH = os.path.join(MN_CFGPATH, MN_VARDIR)
MN_LOCKPATH = os.path.join(MN_VARPATH, MN_LOCKDIR)
MN_RUNPATH = os.path.join(MN_VARPATH, MN_RUNDIR)

#from mininet.clean import cleanup
from mininet.cli import CLI
from mininet.log import info
from mininet.net import Mininet, VERSION

from mininet.node import ( Host, CPULimitedHost, Controller, OVSController,
                           NOX, RemoteController, UserSwitch, OVSKernelSwitch,
                           OVSLegacyKernelSwitch )

from mininet.link import Link, TCLink
from mininet.topo import Topo
from mininet.util import custom, customConstructor, irange, checkInt
#from mininet.util import buildTopo

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
LINKS = { 'default': Link,
          'tc': TCLink }

#preconfigured services
#service description dictionary can have following sets of keys:
#{cmd_start, [start_custom_opts], need_stop = False}
#{cmd_start, [start_custom_opts], need_stop = True, cmd_stop = None }=> (killing by pid)
#{cmd_start, [start_custom_opts], need_stop = True, cmd_stop, [stop_custom_opts]}

SERVICES = { 'dhcpd':   {   'cmd_start': 'dhcpd', 
                            'start_custom_opts': '--no-pid -cf %C/%N/etc/dhcp/dhcpd.mininet.conf',
                            'cmd_stop': None,
                            'need_stop': True
                        },
             'dhcp':	{   'cmd_start': 'dhclient -r  ; ifconfig %h-eth0 0 ; sleep 10 ; dhclient -v --no-pid -lf %C/%N/%h/var/lib/dhcp/dhclient.leases %h-eth0',
                            'need_stop': False
                        },
             'ntpd-srv':{   'cmd_start': 'ntpd',
                            'start_custom_opts': '-c %E/ntp.mininet.server.conf -f %R/ntp.mininet.%h.drift',
                            'cmd_stop': None,
                            'need_stop': True   
			 }, 
             'ntpd-cli':{   'cmd_start': 'ntpd',
                            'start_custom_opts': '-c %E/ntp.mininet.client.conf -f %R/ntp.mininet.%h.drift',
                            'cmd_stop': None,
                            'need_stop': True   
			 } 
}

class cmdStrSubst( object ):
    def __init__(self, escchar = '%', **kwargs):
        self.ec = escchar
        self.hecd = { 'C' : MN_CFGPATH, 'E': MN_ETCPATH, 'V': MN_VARPATH,
                    'L': MN_LOCKPATH, 'R': MN_RUNPATH }
        #%N stands for servicename
        self.reinit(escchar = escchar,**kwargs) 
    
    def reinit(self, escchar = '%', host_obj = None, a_mecd = {}, **kwargs):
        self.ecd = {}
        self.mecd = {}
        self.mecd.update(kwargs)
        self.mecd.update(a_mecd)
        self.ecd[self.ec] = self.ec
        if host_obj:
            self.gen_default_host_dict(host_obj)
        self.ecd.update(self.hecd)
        #manual overlay for dict setup, constants only!
        self.ecd.update(self.mecd)
 
    def gen_default_host_dict(self, host_obj):
        #try block?
        self.hecd['h'] = host_obj.name
        self.hecd['i'] = str(host_obj.IP())        
        self.hecd['m'] = str(host_obj.MAC())
        return self.hecd        

    def res_compile(self):
        self.ecd = {}
        self.ecd[self.ec] = self.ec
        self.ecd.update(self.hecd)
        self.ecd.update(self.mecd)
        #print "res_compile fin dict>>", self.ecd
        return re.compile('(' + self.ec + '[' + "".join(self.ecd.keys()) + '])')

    def repl_concurrent(self, fstr):
        #fstr -- format string to convert 
        #print "repl_concurrent>> "
        self.res = self.res_compile()
        l = self.res.split(fstr) 
        r = map( lambda i: self.ecd.get(i[1], i) \
            if len(i) == 2 and i[0] == self.ec else i, l)
        return "".join(r) 
 
    def add_ec_pair(self, k, v):
        self.mecd[k] = v

    def remove_ec_pair(self, k):
        self.mecd.pop(k, 1)

    def add_ec_pairs(self, **kwargs):
        self.mecd.update(kwargs)

    def add_ec_dict(self, exd):
        self.mecd.update(exd)

    def clean_ec_dict(self):
        self.mecd = {}

#switch s0 supposed to handle all 'special' service hosts 'hs#'
#still one can define services on other hosts, no restrictions
#switch s0 is also a root switch for other switches
class LinearConnectTopo( Topo ):
    "Topology for one linear Mininet segment"

    def __init__( self, N, S, **params ):

        Topo.__init__( self, **params )

        switch = self.addSwitch('s0')
        #server host for sample
        hs = self.addHost( 'hs%s' % '0' )
        self.addLink(hs, switch)

        for sw in irange( 1, S):
            hosts = [ self.addHost( 'h%s' % h ) for h in irange( (sw-1)*N+1, sw*N ) ]
            switchS = self.addSwitch('s'+str(sw)) 
            print(switchS)
            self.addLink(switch, switchS)
            for host in hosts:
                self.addLink(host, switchS)


#devoted services class
class mnServices(object):
    def __init__(self):
        self.services = {}
        #checks for existance on the base of SERVICES progs?
        self.cSP = cmdStrSubst()

    def add_preconf_service(self, hostname, prio, service_id):
        if not checkInt(prio):
            return False
        if service_id not in SERVICES.keys():
            print >> sys.stderr, "Unknown preconfigured service %s" % str(service_id)
            return False
        return self.do_add_service(hostname, int(prio), SERVICES[service_id],
                cSP_cd = {'N':service_id})

    def add_service(self, hostname, prio, service_args_dict, cSP_cdict = None): 
        if not checkInt(prio):
            return False
        #obscure service description dictionary logic check
        if 'cmd_start' not in service_args_dict.keys():
            print >> sys.stderr, "Customized service for %s lacks cmd_start string" % self.h
            return False
        if 'need_stop' not in service_args_dict.keys():
            print >> sys.stderr, "Customized service for %s lacks need_stop bool" % self.h
            return False
        if not service_args_dict['need_stop']:
            return self.do_add_service(hostname, int(prio), service_args_dict)
        #need_stop == False
        if 'cmd_stop' not in service_args_dict.keys():
            print >> sys.stderr, "Customized service for %s lacks cmd_stop bool" % self.h
            return False
        return self.do_add_service(hostname, int(prio), service_args_dict, cSP_cd = cSP_cdict)

    def do_add_service(self, hostname, prio, service_args_dict, cSP_cd = None):
        #services is a dictionary of lists by priority
        #each list contains dictionaries, describing particular service 
        #on particular host instance
        if prio not in self.services.keys():
            self.services[prio] = []
        #prepare entry
        s_entry = service_args_dict.copy()
        s_entry['host'] = hostname
        s_entry['pid'] = None
        s_entry['cSP_cdict'] = cSP_cd
        self.services[prio].append(s_entry)
        print "Service added"
        return True

    def start_services(self, nameToNode):
        for p in sorted(self.services):
            print "Start_services main loop"
 	    os.system( 'tc qdisc add dev eth1 root handle 1:1 netem delay 120ms' )
            for hsi_d in self.services[p]:
                h = nameToNode[hsi_d['host']]
                self.cSP.reinit( host_obj = h )
                if hsi_d['cSP_cdict']:
                    self.cSP.add_ec_dict(hsi_d['cSP_cdict'])
                cmdl = [ hsi_d['cmd_start'] ]
                if 'start_custom_opts' in hsi_d.keys():
                    cmdl.append(hsi_d['start_custom_opts'])
                #no pid back yet!
                #>>regexp
                #print "cmdl to translate: ", cmdl
                cmdfin = map(lambda x: self.cSP.repl_concurrent(x), cmdl)
                #print "cmdfin to launch: " , cmdfin
                h.cmd(cmdfin)
#               h.cmd(map(lambda x: self.cSP.repl_concurrent(x), cmdl))
	    time.sleep(2) #<<Ought to have barrier here
        print "Services started"
        return True

    def stop_services(self, nameToNode):
        for p in sorted(self.services):
            for hsi_d in self.services[p]:
                if not hsi_d['need_stop']:
                    continue
                h = nameToNode[ hsi_d['host'] ]
                self.cSP.reinit( host_obj = h )
                if not hsi_d['cmd_stop']:
                    continue
                cmdl = [ hsi_d['cmd_stop'] ]
                if 'stop_custom_opts' in hsi_d.keys():
                    cmdl.append(hsi_d['stop_custom_opts'])
                #no pid back yet!
                #>>regexp
                #h.cmd(cmdl)
                h.cmd(map(lambda x: self.cSP.repl_concurrent(x), cmdl))
        return True

#wrapper class for Mininet to incorporate services launcher
#'example' style solution only! 
#Normaly ought to be implemented through core classes. Not wrapper!
#
class wrpMininet(Mininet):
    def __init__(self, *pargs, **kwargs):

        #extra args support
        self.service_factory = None 
        self.service_flag = kwargs.pop('services', None)
        if self.service_flag:
            self.service_factory = mnServices()
        Mininet.__init__(self, *pargs, **kwargs)

    def start( self ):
        Mininet.start(self)
        #services unrolling
        self.start_services()

    def stop( self ):
        #services shutdown
        self.stop_services()
        Mininet.stop(self)

    def verify_hostname(self, hostname):
        try:
            h = str(hostname)
            return True
        except ValueError:
            print >> sys.stderror, "Wrong hostname"
            return False
        if h not in self.nameToNode.keys():
            print >> sys.stderr, "Unknown host %s" % h 
            return False
        return True

    def add_preconf_service(self, hostname, *args):
        if self.service_factory and self.verify_hostname(hostname):
            return self.service_factory.add_preconf_service(str(hostname), *args)
        return False

    def add_service(self, hostname, *args): 
        if self.service_factory and self.verify_hostname(hostname):
            return self.service_factory.add_service(str(hostname), *args)
        return False

    def start_services(self):
        if not self.service_factory:
            return False
        ret = self.service_factory.start_services(self.nameToNode)
    	#update IPs of all hosts inside of mininet structures
	    #very dirty fix
        for h in self.hosts:
	        h.defaultIntf().updateIP()
        return ret

    def stop_services(self):
        if not self.service_factory:
            return False
        return self.service_factory.stop_services(self.nameToNode) 

class MininetRunner( object ):
    "Build, setup, and run Mininet."
    def __init__( self ):
        "Init."
        #N -- number of hosts per switch
        #S -- number of switches sitting on root switch
        self.N = 2
        self.S = 3

        self.options = None
        self.args = None  # May be used someday for more CLI scripts
        self.validate = None

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

    def begin( self ):
        "Create and run mininet."

        start = time.time()

        topo = LinearConnectTopo( N = self.N, S = self.S )
        switch = customConstructor( SWITCHES, SWITCHDEF )
        host = customConstructor( HOSTS, HOSTDEF )
        controller = customConstructor( CONTROLLERS, CONTROLLERDEF )
        link = customConstructor( LINKS, LINKDEF )

        inNamespace = False
        Net = wrpMininet
        ipBase = '10.0.0.0/8'
    	listenPort = 6634 

        mn = Net( topo=topo,
                  switch=switch, host=host, controller=controller,
                  link=link,
                  ipBase=ipBase,
                  inNamespace=inNamespace,
                  listenPort=listenPort,
                  services = True)

#Add services here
#        mn.add_preconf_service( 'hs0', 1 , 'dhcpd' )
#ADD cmdStrSubst modification to preconf_service
        #mn.add_preconf_service( 'hs0', 3 , 'ntpd-srv' )
        
#        for swi in irange( 1, self.S):
#            hl = [ ('h%s' % h ) for h in irange((swi - 1) * self.N + 1, swi * self.N) ]
#            for hn in hl:
#                mn.add_preconf_service( hn, 2, 'dhclient' )
                #mn.add_preconf_service( hn, 4, 'ntpd-cli' )

        mn.start()
    	CLI(mn)
        mn.stop()

        elapsed = float( time.time() - start )
        info( 'completed in %0.3f seconds\n' % elapsed )

if __name__ == "__main__":
    MininetRunner()

