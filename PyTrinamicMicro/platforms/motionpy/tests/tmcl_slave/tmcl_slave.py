'''
Test the TMCL_Slave.

Created on 15.12.2020

@author: LK
'''

from PyTrinamicMicro.TMCL_Slave import TMCL_Slave
from PyTrinamicMicro.connections.virtual_tmcl_interface import virtual_tmcl_interface
from PyTrinamic.TMCL import TMCL_Request, TMCL_Reply, TMCL
from PyTrinamic.modules.TMCM0960.TMCM0960 import TMCM0960
import logging
import re
import struct

VERSION_PATTERN = "^\d\d\d\dV\d\d\d$"

logger = logging.getLogger(__name__)

logger.info("Test TMCL_Slave")

logger.info("Initializing virtual interface.")
host = virtual_tmcl_interface()
res = virtual_tmcl_interface()

# Add virtual commands to interface
host.send_request_only(TMCL_Request(1, TMCL.COMMANDS["GET_FIRMWARE_VERSION"], TMCM0960.ENUMs.VERSION_FORMAT_ASCII, 0, 0))
host.send_request_only(TMCL_Request(1, TMCL.COMMANDS["GET_FIRMWARE_VERSION"], TMCM0960.ENUMs.VERSION_FORMAT_BINARY, 0, 0))
host.send_request_only(TMCL_Request(1, TMCL.COMMANDS["GET_FIRMWARE_VERSION"], TMCM0960.ENUMs.VERSION_FORMAT_BUILD, 0, 0))
host.send_request_only(TMCL_Request(1, TMCL.COMMANDS["TMCL_UF0"], 0, 0, 0)) # stop

slave = TMCL_Slave()

c = 0
while(not(slave.status.stop)):
    assert (c < 4), "TMCL_Slave did not stop on stop command"
    if(host.request_available()):
        logger.debug("Request available.")
        request = host.receive_request()
        if(not(slave.filter(request))):
            continue
        logger.debug("Request for this slave detected.")
        reply = slave.handle_request(request)
        res.send_reply(reply)
        c += 1

version_str = ""
if(res.data_available()):
    reply = res.receive_reply()
    version_str = reply.versionString()
    assert re.match(VERSION_PATTERN, version_str), "Invalid version string"
else:
    assert False, "Not enough replies"
if(res.data_available()):
    reply = res.receive_reply()
    version = struct.unpack("BBBB", struct.pack(">I", reply.value))
    assert ((version[0] == int(version_str[0:2])) and (version[1] == int(version_str[2:4]))
        and (version[2] == int(version_str[5:6])) and (version[3] == int(version_str[6:8]))), "Binary version does not match version string"
else:
    assert False, "Not enough replies"
if(res.data_available()):
    reply = res.receive_reply()
else:
    assert False, "Not enough replies"

logger.info("Test completed successfully.")
