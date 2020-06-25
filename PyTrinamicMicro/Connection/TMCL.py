'''
Created on 25.06.2020

@author: LK
'''

from PyTrinamicMicro.TMCL import TMCL_Request, TMCL_Command, TMCL_Reply

from PyTrinamicMicro.helpers import TMC_helpers

class TMCL_Connection():
    def __init__(self, hostID=2, defaultModuleID=1, debug=False):
        if not(type(hostID) == type(defaultModuleID) == int):
            raise TypeError

        if not(0 <= hostID < 256):
            raise ValueError("Incorrect Host ID value")

        if not(0 <= defaultModuleID < 256):
            raise ValueError("Incorrect defaultModule ID value")

        if not type(debug) == bool:
            raise TypeError

        self._HOST_ID    = hostID
        self._MODULE_ID  = defaultModuleID
        self._debug      = debug

    def _send(self, hostID, moduleID, data):
        raise NotImplementedError("The TMCL interface requires an implementation of the _send() function")

    def _recv(self, hostID, moduleID):
        raise NotImplementedError("The TMCL interface requires an implementation of the _recv() function")

    def enableDebug(self, enable):
        if type(enable) != bool:
            raise TypeError("Expected boolean value")

        self._debug = enable

    def send(self, opcode, opType, motor, value, moduleID=None):
        if not(type(opcode) == type(opType) == type(motor) == type(value) == int):
            raise TypeError("Expected integer values")

        if not moduleID:
            moduleID = self._MODULE_ID

        request = TMCL_Request(moduleID, opcode, opType, motor, value)

        if self._debug:
            request.dump()

        self._send(self._HOST_ID, moduleID, request.toBuffer())

        reply = TMCL_Reply(self._recv(self._HOST_ID, moduleID))

        if self._debug:
            reply.dump()

        return reply

    def sendBoot(self, moduleID=None):
        if not moduleID:
            moduleID = self._MODULE_ID

        request = TMCL_Request(moduleID, TMCL_Command.BOOT, 0x81, 0x92, 0xA3B4C5D6)

        if self._debug:
            request.dump()

        self._send(self._HOST_ID, moduleID, request.toBuffer())

    def getVersionString(self, moduleID=None):
        reply = self.send(TMCL_Command.GET_FIRMWARE_VERSION, 0, 0, 0, moduleID)

        return reply.versionString()

    def parameter(self, pCommand, pType, pAxis, pValue, moduleID=None, signed=False):
        value = self.send(pCommand, pType, pAxis, pValue, moduleID).value
        return TMC_helpers.toSigned32(value) if signed else value

    def setParameter(self, pCommand, pType, pAxis, pValue, moduleID=None):
        return self.send(pCommand, pType, pAxis, pValue, moduleID)

    # Axis parameter access functions
    def axisParameter(self, commandType, axis, moduleID=None, signed=False):
        value = self.send(TMCL_Command.GAP, commandType, axis, 0, moduleID).value
        return TMC_helpers.toSigned32(value) if signed else value

    def setAxisParameter(self, commandType, axis, value, moduleID=None):
        return self.send(TMCL_Command.SAP, commandType, axis, value, moduleID)

    def storeAxisParameter(self, commandType, axis, moduleID=None):
        return self.send(TMCL_Command.STAP, commandType, axis, 0, moduleID)

    def setAndStoreAxisParameter(self, commandType, axis, value, moduleID=None):
        self.send(TMCL_Command.SAP, commandType, axis, value, moduleID)
        self.send(TMCL_Command.STAP, commandType, axis, 0, moduleID)

    def globalParameter(self, commandType, bank, moduleID=None, signed=False):
        value = self.send(TMCL_Command.GGP, commandType, bank, 0, moduleID).value
        return TMC_helpers.toSigned32(value) if signed else value

    def setGlobalParameter(self, commandType, bank, value, moduleID=None):
        return self.send(TMCL_Command.SGP, commandType, bank, value, moduleID)

    def storeGlobalParameter(self, commandType, bank, moduleID=None):
        return self.send(TMCL_Command.STGP, commandType, bank, 0, moduleID)

    def setAndStoreGlobalParameter(self, commandType, bank, value, moduleID=None):
        self.send(TMCL_Command.SGP, commandType, bank, value, moduleID)
        self.send(TMCL_Command.STGP, commandType, bank, 0, moduleID)

    def writeMC(self, registerAddress, value, moduleID=None):
        return self.writeRegister(registerAddress, TMCL_Command.WRITE_MC, 0, value, moduleID)

    def readMC(self, registerAddress, moduleID=None, signed=False):
        return self.readRegister(registerAddress, TMCL_Command.READ_MC, 0, moduleID, signed)

    def writeDRV(self, registerAddress, value, moduleID=None):
        return self.writeRegister(registerAddress, TMCL_Command.WRITE_DRV, 1, value, moduleID)

    def readDRV(self, registerAddress, moduleID=None, signed=False):
        return self.readRegister(registerAddress, TMCL_Command.READ_DRV, 1, moduleID, signed)

    def readRegister(self, registerAddress, command, channel, moduleID=None, signed=False):
        value = self.send(command, registerAddress, channel, 0, moduleID).value
        return TMC_helpers.toSigned32(value) if signed else value

    def writeRegister(self, registerAddress, command, channel, value, moduleID=None):
        return self.send(command, registerAddress, channel, value, moduleID)

    def rotate(self, motor, velocity, moduleID=None):
        return self.send(TMCL_Command.ROR, 0, motor, velocity, moduleID)

    def stop(self, motor, moduleID=None):
        return self.send(TMCL_Command.MST, 0, motor, 0, moduleID)

    def move(self, moveType, motor, position, moduleID=None):
        return self.send(TMCL_Command.MVP, moveType, motor, position, moduleID)

    def analogInput(self, x, moduleID=None):
        return self.send(TMCL_Command.GIO, x, 1, 0, moduleID).value

    def digitalInput(self, x, moduleID=None):
        return self.send(TMCL_Command.GIO, x, 0, 0, moduleID).value

    def digitalOutput(self, x, moduleID=None):
        return self.send(TMCL_Command.GIO, x, 2, 0, moduleID).value

    def setDigitalOutput(self, x, moduleID=None):
        self.send(TMCL_Command.SIO, x, 2, 1, moduleID).value

    def clearDigitalOutput(self, x, moduleID=None):
        self.send(TMCL_Command.SIO, x, 2, 0, moduleID).value
