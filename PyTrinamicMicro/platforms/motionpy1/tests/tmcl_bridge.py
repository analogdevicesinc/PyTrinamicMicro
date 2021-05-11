'''
Test TMCL_Bridge.

Created on 18.12.2020

@author: LK
'''

from PyTrinamicMicro import PyTrinamicMicro
from PyTrinamicMicro.connections.virtual_tmcl_interface import virtual_tmcl_interface
from PyTrinamicMicro.TMCL_Bridge import TMCL_Bridge
from PyTrinamic.TMCL import TMCL, TMCL_Request, TMCL_Reply
import logging

# Prepare Logger
logger = logging.getLogger(__name__)
logger.info("Test TMCL_Bridge")

logger.info("Initializing interfaces ...")
host = virtual_tmcl_interface()
modules = [{"module": virtual_tmcl_interface()}]
bridge = TMCL_Bridge(host, modules)
logger.info("Interfaces initialized.")

# Prepare requests
host.send_request_only(TMCL_Request(1, 2, 3, 4, 5))
host.send_request_only(TMCL_Request(3, 2, 3, 4, 5))
host.send_request_only(TMCL_Request(3, TMCL.COMMANDS["TMCL_UF0"], 0, 0, 0)) # stop

# Prepare replies
modules[0]["module"].send_reply(TMCL_Reply(2, 1, 1, 2, 3))

while(not(bridge.process())):
    pass

if(host.data_available()):
    reply = host.receive_reply()
    assert ((reply.reply_address == 2) and (reply.module_address == 1) and (reply.status == 1)
        and (reply.command == 2) and (reply.value == 3)), "Received reply does not match sent reply"
else:
    assert False, "Not enough replies"
if(host.data_available()):
    reply = host.receive_reply()
    assert (reply.status != 100), "Status should not be OK here"
else:
    assert False, "Not enough replies"

logger.info("Closing interfaces ...")
host.close()
for module in modules:
    module["module"].close()
logger.info("Interfaces closed.")

logger.info("Test successful.")
