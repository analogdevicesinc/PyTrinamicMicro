################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

from PyTrinamicMicro.platforms.motionpy2.modules.hc_sr04_multi import hc_sr04_multi
import logging
import time

logger = logging.getLogger(__name__)

distances = [0, 0, 0, 0]
sensor = hc_sr04_multi()

while(True):
    for idx in range(0, len(distances)):
        distances[idx] = sensor.distance(idx)
    logger.info("distances = {}".format(distances))
    time.sleep(0.02)
