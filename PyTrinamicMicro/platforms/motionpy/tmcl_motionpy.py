from PyTrinamicMicro.TMCL_Slave import TMCL_Slave

class tmcl_motionpy(TMCL_Slave):

    def __init__(self, module_address=1, host_address=2, version_string="0960V100", build_version=0):
        super().__init__(module_address, host_address, version_string, build_version)
