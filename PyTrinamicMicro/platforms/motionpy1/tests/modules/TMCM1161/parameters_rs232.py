################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Test TMCL Parameters of TMCM1161 via RS232 interface and module ID 1.

Created on 15.12.2020

@author: LK
'''

from PyTrinamicMicro.platforms.motionpy1.connections.rs232_tmcl_interface import rs232_tmcl_interface
from PyTrinamic.modules.TMCM1161.TMCM_1161 import TMCM_1161
import logging

MODULE_ID = 1
GP_BANK = 0
AP_AXIS = 0

logger = logging.getLogger(__name__)
logger.info("Test module TMCM1161 parameters via RS232")

logger.info("Initializing interface.")
interface = rs232_tmcl_interface(module_id=MODULE_ID)

logger.info("Initializing module.")
module = TMCM_1161(interface)

logger.info("Testing global parameter access.")

logger.info("Getting global parameter ({}, {}) ...".format("timer_0", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.timer_0, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("timer_1", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.timer_1, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("timer_2", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.timer_2, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("stopLeft_0", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.stopLeft_0, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("stopRight_0", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.stopRight_0, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("input_0", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.input_0, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("input_1", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.input_1, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("input_2", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.input_2, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("input_3", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.input_3, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("serialBaudRate", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.serialBaudRate, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("serialAddress", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.serialAddress, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("ASCIIMode", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.ASCIIMode, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("serialHeartbeat", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.serialHeartbeat, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("telegramPauseTime", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.telegramPauseTime, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("serialHostAddress", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.serialHostAddress, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("autoStartMode", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.autoStartMode, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("limitSwitchPolarity", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.limitSwitchPolarity, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("protectionMode", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.protectionMode, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("eepromCoordinateStore", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.eepromCoordinateStore, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("zeroUserVariables", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.zeroUserVariables, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("serialSecondaryAddress", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.serialSecondaryAddress, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("reverseShaftDirection", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.reverseShaftDirection, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("applicationStatus", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.applicationStatus, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("downloadMode", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.downloadMode, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("programCounter", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.programCounter, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("lastTmclError", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.lastTmclError, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("tickTimer", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.tickTimer, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("randomNumber", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.randomNumber, GP_BANK)))
logger.info("Getting global parameter ({}, {}) ...".format("Intpol", module.GPs.timer_0))
logger.info("{}".format(module.getGlobalParameter(module.GPs.Intpol, GP_BANK)))

logger.info("Testing axis parameter access.")

logger.info("Getting axis parameter ({}, {}) ...".format("TargetPosition", module.APs.TargetPosition))
logger.info("{}".format(module.getAxisParameter(module.APs.TargetPosition, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("ActualPosition", module.APs.ActualPosition))
logger.info("{}".format(module.getAxisParameter(module.APs.ActualPosition, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("TargetVelocity", module.APs.TargetVelocity))
logger.info("{}".format(module.getAxisParameter(module.APs.TargetVelocity, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("ActualVelocity", module.APs.ActualVelocity))
logger.info("{}".format(module.getAxisParameter(module.APs.ActualVelocity, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("MaxVelocity", module.APs.MaxVelocity))
logger.info("{}".format(module.getAxisParameter(module.APs.MaxVelocity, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("MaxAcceleration", module.APs.MaxAcceleration))
logger.info("{}".format(module.getAxisParameter(module.APs.MaxAcceleration, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("MaxCurrent", module.APs.MaxCurrent))
logger.info("{}".format(module.getAxisParameter(module.APs.MaxCurrent, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("StandbyCurrent", module.APs.StandbyCurrent))
logger.info("{}".format(module.getAxisParameter(module.APs.StandbyCurrent, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("PositionReachedFlag", module.APs.PositionReachedFlag))
logger.info("{}".format(module.getAxisParameter(module.APs.PositionReachedFlag, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("referenceSwitchStatus", module.APs.referenceSwitchStatus))
logger.info("{}".format(module.getAxisParameter(module.APs.referenceSwitchStatus, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("RightEndstop", module.APs.RightEndstop))
logger.info("{}".format(module.getAxisParameter(module.APs.RightEndstop, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("LeftEndstop", module.APs.LeftEndstop))
logger.info("{}".format(module.getAxisParameter(module.APs.LeftEndstop, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("rightLimitSwitchDisable", module.APs.rightLimitSwitchDisable))
logger.info("{}".format(module.getAxisParameter(module.APs.rightLimitSwitchDisable, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("leftLimitSwitchDisable", module.APs.leftLimitSwitchDisable))
logger.info("{}".format(module.getAxisParameter(module.APs.leftLimitSwitchDisable, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("minimumSpeed", module.APs.minimumSpeed))
logger.info("{}".format(module.getAxisParameter(module.APs.minimumSpeed, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("actualAcceleration", module.APs.actualAcceleration))
logger.info("{}".format(module.getAxisParameter(module.APs.actualAcceleration, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("RampMode", module.APs.RampMode))
logger.info("{}".format(module.getAxisParameter(module.APs.RampMode, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("MicrostepResolution", module.APs.MicrostepResolution))
logger.info("{}".format(module.getAxisParameter(module.APs.MicrostepResolution, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("Ref_SwitchTolerance", module.APs.Ref_SwitchTolerance))
logger.info("{}".format(module.getAxisParameter(module.APs.Ref_SwitchTolerance, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("softStopFlag", module.APs.softStopFlag))
logger.info("{}".format(module.getAxisParameter(module.APs.softStopFlag, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("EndSwitchPowerDown", module.APs.EndSwitchPowerDown))
logger.info("{}".format(module.getAxisParameter(module.APs.EndSwitchPowerDown, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("rampDivisor", module.APs.rampDivisor))
logger.info("{}".format(module.getAxisParameter(module.APs.rampDivisor, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("PulseDivisor", module.APs.PulseDivisor))
logger.info("{}".format(module.getAxisParameter(module.APs.PulseDivisor, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("Intpol", module.APs.Intpol))
logger.info("{}".format(module.getAxisParameter(module.APs.Intpol, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("DoubleEdgeSteps", module.APs.DoubleEdgeSteps))
logger.info("{}".format(module.getAxisParameter(module.APs.DoubleEdgeSteps, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("ChopperBlankTime", module.APs.ChopperBlankTime))
logger.info("{}".format(module.getAxisParameter(module.APs.ChopperBlankTime, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("ConstantTOffMode", module.APs.ConstantTOffMode))
logger.info("{}".format(module.getAxisParameter(module.APs.ConstantTOffMode, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("DisableFastDecayComparator", module.APs.DisableFastDecayComparator))
logger.info("{}".format(module.getAxisParameter(module.APs.DisableFastDecayComparator, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("ChopperHysteresisEnd", module.APs.ChopperHysteresisEnd))
logger.info("{}".format(module.getAxisParameter(module.APs.ChopperHysteresisEnd, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("ChopperHysteresisStart", module.APs.ChopperHysteresisStart))
logger.info("{}".format(module.getAxisParameter(module.APs.ChopperHysteresisStart, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("TOff", module.APs.TOff))
logger.info("{}".format(module.getAxisParameter(module.APs.TOff, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("SEIMIN", module.APs.SEIMIN))
logger.info("{}".format(module.getAxisParameter(module.APs.SEIMIN, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("SECDS", module.APs.SECDS))
logger.info("{}".format(module.getAxisParameter(module.APs.SECDS, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("smartEnergyHysteresis", module.APs.smartEnergyHysteresis))
logger.info("{}".format(module.getAxisParameter(module.APs.smartEnergyHysteresis, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("SECUS", module.APs.SECUS))
logger.info("{}".format(module.getAxisParameter(module.APs.SECUS, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("smartEnergyHysteresisStart", module.APs.smartEnergyHysteresisStart))
logger.info("{}".format(module.getAxisParameter(module.APs.smartEnergyHysteresisStart, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("SG2FilterEnable", module.APs.SG2FilterEnable))
logger.info("{}".format(module.getAxisParameter(module.APs.SG2FilterEnable, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("SG2Threshold", module.APs.SG2Threshold))
logger.info("{}".format(module.getAxisParameter(module.APs.SG2Threshold, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("slopeControlHighSide", module.APs.slopeControlHighSide))
logger.info("{}".format(module.getAxisParameter(module.APs.slopeControlHighSide, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("slopeControlLowSide", module.APs.slopeControlLowSide))
logger.info("{}".format(module.getAxisParameter(module.APs.slopeControlLowSide, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("ShortToGroundProtection", module.APs.ShortToGroundProtection))
logger.info("{}".format(module.getAxisParameter(module.APs.ShortToGroundProtection, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("ShortDetectionTime", module.APs.ShortDetectionTime))
logger.info("{}".format(module.getAxisParameter(module.APs.ShortDetectionTime, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("VSense", module.APs.VSense))
logger.info("{}".format(module.getAxisParameter(module.APs.VSense, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("smartEnergyActualCurrent", module.APs.smartEnergyActualCurrent))
logger.info("{}".format(module.getAxisParameter(module.APs.smartEnergyActualCurrent, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("smartEnergyStallVelocity", module.APs.smartEnergyStallVelocity))
logger.info("{}".format(module.getAxisParameter(module.APs.smartEnergyStallVelocity, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("smartEnergyThresholdSpeed", module.APs.smartEnergyThresholdSpeed))
logger.info("{}".format(module.getAxisParameter(module.APs.smartEnergyThresholdSpeed, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("smartEnergySlowRunCurrent", module.APs.smartEnergySlowRunCurrent))
logger.info("{}".format(module.getAxisParameter(module.APs.smartEnergySlowRunCurrent, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("RandomTOffMode", module.APs.RandomTOffMode))
logger.info("{}".format(module.getAxisParameter(module.APs.RandomTOffMode, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("ReferenceSearchMode", module.APs.ReferenceSearchMode))
logger.info("{}".format(module.getAxisParameter(module.APs.ReferenceSearchMode, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("ReferenceSearchSpeed", module.APs.ReferenceSearchSpeed))
logger.info("{}".format(module.getAxisParameter(module.APs.ReferenceSearchSpeed, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("referenceSwitchSpeed", module.APs.referenceSwitchSpeed))
logger.info("{}".format(module.getAxisParameter(module.APs.referenceSwitchSpeed, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("referenceSwitchDistance", module.APs.referenceSwitchDistance))
logger.info("{}".format(module.getAxisParameter(module.APs.referenceSwitchDistance, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("lastReferenceSwitchPosition", module.APs.lastReferenceSwitchPosition))
logger.info("{}".format(module.getAxisParameter(module.APs.lastReferenceSwitchPosition, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("BoostCurrent", module.APs.BoostCurrent))
logger.info("{}".format(module.getAxisParameter(module.APs.BoostCurrent, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("freewheelingDelay", module.APs.freewheelingDelay))
logger.info("{}".format(module.getAxisParameter(module.APs.freewheelingDelay, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("LoadValue", module.APs.LoadValue))
logger.info("{}".format(module.getAxisParameter(module.APs.LoadValue, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("extendedErrorFlags", module.APs.extendedErrorFlags))
logger.info("{}".format(module.getAxisParameter(module.APs.extendedErrorFlags, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("DrvStatusFlags", module.APs.DrvStatusFlags))
logger.info("{}".format(module.getAxisParameter(module.APs.DrvStatusFlags, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("EncoderPosition", module.APs.EncoderPosition))
logger.info("{}".format(module.getAxisParameter(module.APs.EncoderPosition, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("EncoderResolution", module.APs.EncoderResolution))
logger.info("{}".format(module.getAxisParameter(module.APs.EncoderResolution, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("max_EncoderDeviation", module.APs.max_EncoderDeviation))
logger.info("{}".format(module.getAxisParameter(module.APs.max_EncoderDeviation, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("PowerDownDelay", module.APs.PowerDownDelay))
logger.info("{}".format(module.getAxisParameter(module.APs.PowerDownDelay, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("absoluteResolverValue", module.APs.absoluteResolverValue))
logger.info("{}".format(module.getAxisParameter(module.APs.absoluteResolverValue, AP_AXIS)))
logger.info("Getting axis parameter ({}, {}) ...".format("Step_DirectionMode", module.APs.Step_DirectionMode))
logger.info("{}".format(module.getAxisParameter(module.APs.Step_DirectionMode, AP_AXIS)))

logger.info("Test completed successfully.")
