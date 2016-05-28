#!/usr/bin/env python 
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os,csv
''' Add your imports here ... '''



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]

''' Add your global variables here ... '''



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):
        ''' Add your logic here ... '''
        #--Read through csv file----#
        f = open(policyFile)
        csv_f = csv.reader(f)
        for row in csv_f:
                if 'id' not in row:
                        src_mac=row[1]
                        dest_mac=row[2]
                        new_match = of.ofp_match()
                        new_match.dl_src= EthAddr(src_mac)
                        new_match.dl_dst= EthAddr(dest_mac)

                        #---Create flow with this match---#
                        msg = of.ofp_flow_mod()
                        msg.match= new_match
                        event.connection.send(msg)




        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)


