################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Interface to the TMCL module.

Created on 05.02.2021

@author: LK
'''

from PyTrinamic.connections.tmcl_interface import tmcl_interface

class tmcl_module_interface(tmcl_interface):

    def data_available(self, host_id=None, module_id=None):
        raise NotImplementedError()

    def reply_available(self, host_id=None, module_id=None):
        return self.data_available(host_id, module_id)
