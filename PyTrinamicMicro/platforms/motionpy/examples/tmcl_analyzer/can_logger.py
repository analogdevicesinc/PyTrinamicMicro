from PyTrinamicMicro.tmcl_analyzer import tmcl_analyzer
from PyTrinamicMicro.platforms.motionpy.connections.can_tmcl_interface import can_tmcl_interface, CanModeSilent
import logging

# Prepare Logger
logger = logging.getLogger(__name__)
logger.info("CAN Logger")

# Callback for received requests
def callback_request(request):
    logger.info(request.disassemble())

# Callback for received replies
def callback_reply(reply):
    logger.info(reply.disassemble())

logger.info("Initializing interface ...")
bus = can_tmcl_interface(host_id=2, module_id=1, can_mode=CanModeSilent())
logger.info("Interface initialized.")

logger.info("Initializing tmcl_analyzer ...")
# Set callback to print disassembled TMCL requests and their replies
# Set measurement window for throughput to 100 ms (not requested but nice to have)
analyzer = tmcl_analyzer(connection_host=bus, connection_module=bus, callback_request=callback_request, callback_reply=callback_reply, measure_window=0.1)
logger.info("tmcl_analyzer initialized.")

logger.info("Start logging.")

# Main loop
while(True):
    analyzer.process()
