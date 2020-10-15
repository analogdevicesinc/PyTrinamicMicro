'''
Utility class to interfere with the bootloader on modules.

Created on 15.10.2020

@author: LK
'''

import io
import logging
import struct

class ihex(object):

    RECORD_STRUCT = "BHB{data}B"

    def __init__(self, file):
        self.__file = file
        self.__logger = logging.getLogger(self.__module__)

    def verify(self, module=None):
        del module

        extendedAddress = 0
        segmentAddress  = 0
        for lineNumber, line in enumerate(self.__file, 1):
            self.__logger.debug("Verifying line {} ...".format(lineNumber))
            ### Parse a hex file line
            # Check for RECORD MARK
            if line[0] != ':':
                self.__logger.debug("No record, continuing.")
                continue

            # CHKSUM validation
            # All Bytes summed together modulo 256 have to be 0
            self.__logger.debug("Verifying checksum ...")
            checksum = 0
            for i in range(1, len(line)-1, 2):
                checksum = checksum + int(line[i:i+2], 16)
            if checksum % 256 != 0:
                raise ValueError("Line {}: Invalid Checksum.".format(lineNumber))
            self.__logger.debug("Checksum OK.")

            # Read the fields of the entry
            rec_len      = int(line[1:3], 16)
            rec_address  = int(line[3:7], 16)
            rec_type     = int(line[7:9], 16)
            rec_data     = line[9:rec_len*2+9]
            self.__logger.debug("Record: (RECLEN = {}, LOAD_OFFSET = {}, RECTYPE = {}, DATA = {})".format(
                rec_len, rec_address, rec_type, rec_data
            ))

            self.__logger.debug("Verifying RECLEN ...")
            # RECLEN validation
            # Total characters:
            #     1: RECORD MARK
            #     2: RECLEN
            #     4: LOAD OFFSET
            #     2: RECTYPE
            #     RECLEN*2: DATA / INFO
            #     2: CHKSUM
            #     1: \n
            if 1 + 2 + 4 + 2 + (rec_len*2) + 2 + 1 != len(line):
                raise ValueError("Line {}: Invalid record length. (rec_len = {}, len = {})".format(lineNumber, rec_len, len(line)))
            self.__logger.debug("RECLEN OK.")

            ### Record type distinction
            self.__logger.debug("Distinguish RECTYPE ...")
            if rec_type == 0:
                # Type: Data Record
                address = extendedAddress + segmentAddress + rec_address
                if address % 4 != 0:
                    raise ValueError("Line {}: Address is not 4-byte aligned. (address = {})".format(lineNumber, address))

            if rec_type == 1:
                # Type: End of File Record
                break

            if rec_type == 2:
                # Type: Extended Segment Address Record
                segmentAddress = int(rec_data, 16) * 0x10

                if extendedAddress != 0:
                    self.__logger.warning("Hex file uses both Type 2 and Type 4 records.")

            if rec_type == 3:
                # Type: Start Segment Address Record
                # Ignore this record
                pass

            if rec_type == 4:
                # Type: Extended Linear Address Record
                extendedAddress = int(rec_data, 16) * 0x10000

                if segmentAddress != 0:
                    self.__logger.warning("Hex file uses both Type 2 and Type 4 records.")

            if rec_type == 5:
                # Type: Start Linear Address Record
                # Ignore this record
                pass

            self.__logger.debug("RECTYPE OK.")

            self.__logger.debug("Line {} OK.".format(lineNumber))

        self.__file.seek(0)
        self.__logger.info("Verified {} lines.".format(lineNumber))

        def read_record(self):
            line = self.__file.readline()[1:-1]
            arr = bytearray(int(len(line) / 2))
            if(line):
                for i in range(0, len(arr)):
                    arr[i] = int(line[(2*i):((2*i)+2)], 16)
                return struct.unpack(RECORD_STRUCT.format(data=("B" * arr[0])), arr)
            return None

        def seek(self, offset):
            if(offset != 0):
                raise ValueError("Random access is not supported.")
            self.__file.seek(offset)


class tmcl_bootloader(object):

    def __init__(self, interface, module=None):
        self.__interface = interface
        self.__module = module

    def update_firmware(self, file):
        hex_file = ihex(file)
        hex_file.verify(self.__module)
