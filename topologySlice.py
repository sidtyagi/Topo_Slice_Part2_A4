'''
Coursera:
- Software Defined Networking (SDN) course
-- Network Virtualization

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
from collections import defaultdict

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree

from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from collections import namedtuple
import os
from pox.core import core

log = core.getLogger()


class TopologySlice (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Slicing Module")


    """This event will be raised each time a switch will connect to the controller"""
    def _handle_ConnectionUp(self, event):

        # Use dpid to differentiate between switches (datapath-id)
        # Each switch has its own flow table. As we'll see in this
        # example we need to write different rules in different tables.
        dpid = dpidToStr(event.dpid)
        log.debug("Switch %s has come up.", dpid)

        """ Add your logic here """
	#----We need to isolate the upper slice from the lower slice
	'''Logic used is as follows-------
	a.Refer each switch by its data path id
	b.Create flows for each switch such that flow from upper slice never reaches
		the lower slice and vice versa'''
	def create_flow(inp_p,out_p):
		fm = of.ofp_flow_mod()  
		fm.match.in_port = inp_p  
		fm.actions.append(of.ofp_action_output(port = out_p))
		return fm
		
	if dpid == '00-00-00-00-00-01' or dpid == '00-00-00-00-00-04':
		log.debug(" Setting flow entry for Switch %s ", dpid)
	
		#--Flow for upper slice---#
		flow_msg1=create_flow(1,3)
		event.connection.send(flow_msg1)
		flow_msg2=create_flow(3,1)
		event.connection.send(flow_msg2)
		#--Flow for lower slice---#
		flow_msg3=create_flow(4,2)
		event.connection.send(flow_msg3)
		flow_msg4=create_flow(2,4)	
		event.connection.send(flow_msg4)
	elif dpid == '00-00-00-00-00-02' or dpid == '00-00-00-00-00-03':
		log.debug(" Setting flow entry for Switch %s ", dpid)
		flow_msg5=create_flow(1,2)
		event.connection.send(flow_msg5)
		flow_msg6=create_flow(2,1)
		event.connection.send(flow_msg6)





def launch():
    # Run spanning tree so that we can deal with topologies with loops
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    '''
    Starting the Topology Slicing module
    '''
    core.registerNew(TopologySlice)
