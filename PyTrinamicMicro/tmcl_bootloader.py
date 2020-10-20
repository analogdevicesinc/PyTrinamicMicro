'''
Utility class to interfere with the bootloader on modules.

Created on 15.10.2020

@author: LK
'''

import io
import logging
import struct
import re
import math
import time
from PyTrinamic.TMCL import TMCL_Command, TMCL_Request, TMCL_Reply

class ihex(object):

    RECORD_STRUCT = ">BHB{data}B"

    def __init__(self, file):
        self.__file = file
        self.start_address = 0
        self.end_address = 0
        self.length = 0
        self.checksum = 0
        self.relative = 0
        self.__logger = logging.getLogger(self.__module__)

    def parse(self):
        extendedAddress = 0
        segmentAddress  = 0
        for lineNumber, line in enumerate(self.__file, 1):
            self.__logger.debug("Parsing line {} ...".format(lineNumber))
            ### Parse a hex file line
            # Check for RECORD MARK
            if line[0] != ':':
                self.__logger.debug("Line {}: No record, continuing.".format(lineNumber))
                continue

            # CHKSUM validation
            # All Bytes summed together modulo 256 have to be 0
            self.__logger.debug("Verifying checksum ...")
            checksum = 0
            for i in range(1, len(line)-1, 2):
                checksum = checksum + int(line[i:i+2], 16)
            if checksum % 256 != 0:
                raise ValueError("Line {}: Invalid Checksum.".format(lineNumber))
            self.__logger.debug("Line {}: Checksum OK.".format(lineNumber))

            # Read the fields of the entry
            rec_len      = int(line[1:3], 16)
            rec_address  = int(line[3:7], 16)
            rec_type     = int(line[7:9], 16)
            rec_data     = line[9:rec_len*2+9]
            self.__logger.debug("Record: (RECLEN = {}, LOAD_OFFSET = {}, RECTYPE = {}, DATA = {})".format(
                rec_len, rec_address, rec_type, rec_data
            ))

            self.__logger.debug("Line {}: Verifying RECLEN ...".format(lineNumber))
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
            self.__logger.debug("Line {}: RECLEN OK.".format(lineNumber))

            ### Record type distinction
            self.__logger.debug("Line {}: Distinguish RECTYPE ...".format(lineNumber))
            if rec_type == 0:
                # Type: Data Record
                if(extendedAddress < 1048576):
                    address = extendedAddress + segmentAddress + rec_address
                    if address % 4 != 0:
                        raise ValueError("Line {}: Address is not 4-byte aligned. (address = {})".format(lineNumber, address))
                    if(not(self.start_address)):
                        self.start_address = address
                        self.relative = extendedAddress + segmentAddress
                    self.end_address = max(address + rec_len, self.end_address)
                    for i in range(0, rec_len * 2, 2):
                        self.checksum = (self.checksum + int(rec_data[i:i+2], 16)) & 0xFFFFFFFF

            if rec_type == 1:
                # Type: End of File Record
                break

            if rec_type == 2:
                # Type: Extended Segment Address Record
                segmentAddress = int(rec_data, 16) * 0x10

                if extendedAddress != 0:
                    self.__logger.warning("Line {}: Hex file uses both Type 2 and Type 4 records.".format(lineNumber))

            if rec_type == 3:
                # Type: Start Segment Address Record
                # Ignore this record
                pass

            if rec_type == 4:
                # Type: Extended Linear Address Record
                extendedAddress = int(rec_data, 16) * 0x10000

                if segmentAddress != 0:
                    self.__logger.warning("Line {}: Hex file uses both Type 2 and Type 4 records.".format(lineNumber))

            if rec_type == 5:
                # Type: Start Linear Address Record
                # Ignore this record
                pass

            self.__logger.debug("Line {}: RECTYPE OK.".format(lineNumber))

            self.__logger.debug("Line {} OK.".format(lineNumber))

        self.length = self.end_address - self.start_address
        self.seek(0)
        self.__logger.info("Parsed {} lines.".format(lineNumber))

        self.__logger.info("Start address: relative 0x{0:08X}, absolute 0x{1:08X}.".format(self.start_address - self.relative, self.start_address))
        self.__logger.info("End address: relative 0x{0:08X}, absolute 0x{1:08X}.".format(self.end_address - self.relative, self.end_address))
        self.__logger.info("Length: 0x{0:08X}.".format(self.length))
        self.__logger.info("Checksum: 0x{0:08X}.".format(self.checksum))

    def read_record(self):
        line = self.__file.readline()[1:-1]
        arr = bytearray(int(len(line) / 2))
        if(line):
            for i in range(0, len(arr)):
                arr[i] = int(line[(2*i):((2*i)+2)], 16)
            return struct.unpack(self.RECORD_STRUCT.format(data=("B" * arr[0])), arr)
        return None

    def seek(self, offset):
        if(offset != 0):
            raise ValueError("Random access is not supported.")
        self.__file.seek(offset)


class tmcl_bootloader(object):

    def __init__(self, interface, module_id=None):
        self.__interface = interface
        self.__module_id = module_id
        self.__mem_page_size = 0
        self.__mem_start_address = 0
        self.__mem_size = 0
        self.__logger = logging.getLogger(self.__module__)

    def verify(self, hex_file):
        self.__logger.info("Verifying bootloader/firmware versions ...")

        skip_version_scan = False
        bootloader_version = self.__interface.getVersionString(1)
        self.__logger.debug("Bootloader version: {}.".format(bootloader_version))
        pattern = ""
        found = re.search("\d\d\d\dB\d\d\d", bootloader_version)
        if found:
            pattern = found.group(0)[0:4] + "V\d\d\d"
            self.__logger.debug("Bootloader pattern: {}.".format(pattern))
        else:
            found = re.search("\d\d\dB\d\.\d\d", bootloader_version)
            if found:
                pattern = found.group(0)[0:3] + "V\d\.\d\d"
                self.__logger.debug("Bootloader pattern: {}.".format(pattern))
            else:
                self.__logger.warning("get_version returned invalid answer for bootloader version: {}.".format(bootloader_version))
                skip_version_scan = True

        if(not(skip_version_scan)):
            # Read 2 records, since firmware version string can be overlapping between 2 records
            record = [hex_file.read_record(), hex_file.read_record()]
            while((record[0] is not None) and (record[1] is not None)):
                # Concatenate the records and get ascii string
                conc_str = bytearray(record[0][3:-1] + record[1][3:-1]).decode("ascii", "ignore")
                found = re.search(pattern, conc_str)
                if(found):
                    self.__logger.debug("Firmware version {} found.".format(found.group(0)))
                    break
                record = [record[1], hex_file.read_record()]
            else:
                raise ValueError("No matching firmware version found in image. ({})".format(pattern))

        hex_file.seek(0)
        self.__logger.info("Bootloader/firmware versions verified.")

        self.__logger.info("Verifying memory addressing ...")

        # Get the memory parameters
        reply = self.__interface.send(TMCL_Command.BOOT_GET_INFO, 0, 0, 0)
        self.__mem_page_size = reply.value
        reply = self.__interface.send(TMCL_Command.BOOT_GET_INFO, 1, 0, 0)
        self.__mem_start_address = reply.value
        reply = self.__interface.send(TMCL_Command.BOOT_GET_INFO, 2, 0, 0)
        self.__mem_size = reply.value

        # Check if the page size is a power of two
        if not(((self.__mem_page_size & (self.__mem_page_size - 1)) == 0) and self.__mem_page_size != 0):
            raise ValueError("Page size of module is not a power of two. Page size: {0:X}.".format(self.__mem_page_size))

        # Check if the start addresses match
        if hex_file.start_address != self.__mem_start_address:
            raise ValueError("Start address of firmware (0x{0:08X}) does not match start address of bootloader (0x{1:08X}).".format(hex_file.start_address, self.__mem_start_address))

        self.__logger.info("Memory addressing verified.")

    def update_firmware(self, file, start=False, checksum_error=True):
        self.__logger.info("Updating firmware ...")

        hex_file = ihex(file)
        hex_file.parse()

        self.__logger.info("Verifying firmware ...")
        self.verify(hex_file)
        self.__logger.info("Firmware verified.")

        self.__logger.info("Erasing old firmware ...")
        self.__interface.send_request(TMCL_Request(self.__module_id, TMCL_Command.BOOT_ERASE_ALL, 0, 0, 0))
        time.sleep(5.0)
        self.__logger.info("Old firmware erased.")

        self.__logger.info("Flashing new firmware ...")
        # Calculate the starting page
        current_page = math.floor(hex_file.start_address / self.__mem_page_size) * self.__mem_page_size
        # Store the internal page buffer state
        current_page_dirty  = False
        record = hex_file.read_record()
        extendedAddress = 0
        segmentAddress = 0
        while(record is not None):
            ### Record type distinction
            if record[2] == 0:
                # Type: Data Record
                if(extendedAddress < 1048576):
                    address = extendedAddress + segmentAddress + record[1]
                    address -= hex_file.relative
                    for i in range(0, record[0], 4):
                        page = math.floor(address / self.__mem_page_size) * self.__mem_page_size
                        offset = address + i - page
                        if page != current_page:
                            self.__logger.info("Writing page {0:08X} ...".format(current_page))
                            self.__interface.send(TMCL_Command.BOOT_WRITE_PAGE, 0, 0, current_page)
                            self.__logger.info("Page {0:08X} written.".format(current_page))
                            current_page = page
                            current_page_dirty = False
                        self.__interface.send(TMCL_Command.BOOT_WRITE_BUFFER, (offset >> 2) % 256, ((offset >> 2) >> 8) % 256, struct.unpack("<I", bytearray(record[(i+3):(i+7)]))[0])
                        current_page_dirty = True
            if record[2] == 2:
                # Type: Extended Segment Address Record
                segmentAddress = struct.unpack(">H", bytearray(record[3:-1]))[0] * 0x10
            if record[2] == 4:
                # Type: Extended Linear Address Record
                extendedAddress = struct.unpack(">H", bytearray(record[3:-1]))[0] * 0x10000
            record = hex_file.read_record()
        # If the last page didn't get written yet, write it
        if current_page_dirty:
            self.__logger.info("Writing page {0:08X} ...".format(current_page))
            self.__interface.send(TMCL_Command.BOOT_WRITE_PAGE, 0, 0, current_page)
            self.__logger.info("Page {0:08X} written.".format(current_page))
        self.__logger.info("Firmware flashed.")

        self.__logger.info("Comparing checksums ...")
        # Checksum verification
        self.__logger.debug("Read checksum at address {0:08X} ...".format(self.__mem_start_address + hex_file.length - 1))
        checksum = 0
        for i in range(0, 3):
            reply = self.__interface.send(TMCL_Command.BOOT_GET_CHECKSUM, 0, 0, self.__mem_start_address + hex_file.length - 1)
            if(reply.value == hex_file.checksum):
                self.__logger.info("Checksums match.")
                checksum = hex_file.checksum
                break
            else:
                self.__logger.warning("Checksums do not match. Retrying. (Hex file: 0x{0:08X}, Firmware: 0x{1:08X})".format(hex_file.checksum, reply.value))
                checksum = reply.value
                time.sleep(1.0)
        else:
            if(checksum_error):
                raise ValueError("Checksums did not match after 3 trials. Aborting firmware update.")
            else:
                self.__logger.warning("Checksums did not match after 3 trials. Writing received checksum 0x{0:08X}.".format(checksum))
        self.__logger.info("Checksums compared.")

        self.__logger.info("Finalizing upload ...")
        # Write firmware length
        self.__interface.send(TMCL_Command.BOOT_WRITE_LENGTH, 0, 0, hex_file.length)
        # Write firmware checksum
        self.__interface.send(TMCL_Command.BOOT_WRITE_LENGTH, 1, 0, checksum)
        self.__logger.info("Upload finalized.")

        self.__logger.info("Firmware updated.")

        if(start):
            self.__logger.info("Starting application ...")
            self.start_application()

    def start_application(self):
        self.__interface.send_request(TMCL_Request(self.__module_id, TMCL_Command.BOOT_START_APPL, 0, 0, 0))
