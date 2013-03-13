#!/usr/bin/env python
# encoding: utf-8
"""
This file is part of pyBusPirate2
Download at http://code.google.com/p/pybuspirate2/

Copyright (c) 2010 Sebastian Muniz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
#
# TODO / FIXME:
#
# [-] Duplicated 'enter BBIO mode' sent.
# [+] main() function code.

__version__     = "0.1"
__author__      = "Sebastian 'topo' Muniz"

__all__         = [ "PinCfg",
                    "BitBangIOPins",
                    "BitBangIOException",
                    "BitBangIO",
                    "BusMode"]

from serial             import Serial, SerialException
from select             import select

class PinCfg:
    """Configuration for each pin in the Bus Pirate board."""
    POWER   = 0x8
    PULLUPS = 0x4
    AUX     = 0x2
    CS      = 0x1

class BitBangIOPins:
    """Bits are assigned to each pin in the Bus Pirate board."""
    MOSI    = 0x01
    CLK     = 0x02
    MISO    = 0x04
    CS      = 0x08
    AUX     = 0x10
    PULLUP  = 0x20
    POWER   = 0x40

class BusMode:
    SPI         = 0x1   # 0b00000001 - Enter binary SPI mode, responds "SPI1"
    I2C         = 0x2   # 0b00000010 - Enter binary I2C mode, responds "I2C1"
    UART        = 0x3   # 0b00000011 - Enter binary UART mode, responds "ART1"
    ONE_WIRE    = 0x4   # 0b00000100 - Enter binary 1-Wire mode, responds "1W01"
    RAW_WIRE    = 0x5   # 0b00000101 - Enter binary raw-wire mode, responds "RAW1"

    MODES = [   SPI,
                I2C,
                UART,
                ONE_WIRE,
                RAW_WIRE ]

    def isSupportedMode(self, mode):
        """Return a boolean indicating if the specified mode is valid or
        not."""
        return bool(mode in self.MODES)

class BitBangIOException(Exception):
    """Standard BinBangIO class exception."""
    pass

class BitBangIO:
    """This class implements the binary bitbang mode protocol to talk to the
    Bus Pirate."""

    """
    [+] 00000000 - Reset, responds "BBIO1"
    [+] 0000xxxx - Reserved for future raw protocol modes
    [+] 00001111 - Reset Bus Pirate (returns to user terminal)
    [-] 00010100 - Take voltage probe measurement (returns 2 bytes)
    [-] 010xxxxx - Set pins as input(1) or output(0), responds with read
    [-] 1xxxxxxx - Set pins high (1) or low (0), responds with read 
    """

    # Perform an automatic convertion from numeric values to strings before
    # being transfered.
    __PERFORM_NUM_TO_STR_CONVERTION = True

    __BIT_BANG_IO_MODE              = "BBIO1"
    __BBIO_CMD_RESET                = 0x0
    __BBIO_CMD_RESET_BP             = 0xF # 0b00001111

    DEFAULT_WAIT_TIMEOUT_SECS       = 0.1
    DEFAULT_BP_PORT_TIMEOUT_SECS    = 0.5

    def __init__(self, port="/dev/bus_pirate", speed=115200,
        time_out=DEFAULT_BP_PORT_TIMEOUT_SECS):
        """Initialize the BitBang IO mode instance."""

        # Set the initialization flag to False because it's setted to True when
        # the Bus Pirate successfully enters in BitBang mode.
        self.__init_ok          = False

        # Set debug flag (Turn it off after development).
        self.__debug_info       = False
        self.__debug_traffic    = False

        try:
            # Initialize the serial port module to comunicate with the bus pirate.
            self.port       = Serial(port, speed, timeout=time_out)
        except SerialException, err:
            raise BitBangIOException(err)

        # Enter the BitBang IO mode to start interacting with the bus pirate.
        if self.__debug_info:
            print "[+] Entering BitBang I/O mode..."

        self.__enterBitBangMode()
    
    def verbose(self, state=True):
        """Set or remove the debugging information output."""
        self.__debug_info = state

    def __del__(self):
        """Restore the Bus Pirate to the user terminal before leaving."""
        # Reset the Bus Pirate.
        if self.__debug_info:
            print "[+] Restoring Bus Pirate to user terminal..."

        if self.__init_ok:
            self.__exitBitBangMode()

    def getVersion(self):
        """Return the version number of the BitBang protocol."""
        return self.version

    def setVersion(self, version):
        """Store the version number of the BitBang protocol."""
        self.version = version

    def flushInput(self):
        """..."""
        # FIXME: Serial operations must be moved to a separate class.
        # TODO: Add abstract class for redirection.
        while True:
            if self.recv(1000, True) in ['', None]:
                break

    def __enterBitBangMode(self):
        """Initialize the Bus Pirate in BitBang mode to send binary
        commands instead of using the interactive user interface provided."""

        # This command resets the Bus Pirate into raw bitbang mode from the
        # user terminal. It also resets to raw bitbang mode from raw SPI mode,
        # or any other protocol mode. This command always returns a five byte
        # bitbang version string "BBIOx", where x is the current protocol
        # version (currently 1).
        #
        # Some terminals send a NULL character (0x00) on start-up, causing the
        # Bus Pirate to enter binary mode when it wasn't wanted. To get around
        # this, you must now enter 0x00 at least 20 times to enter raw bitbang
        # mode.
        #
        # Note: The Bus Pirate user terminal could be stuck in a configuration
        # menu when your program attempts to enter binary mode. One way to
        # ensure that you're at the command line is to send <enter> at least 10
        # times, and then send '#' to reset. Next, send 0x00 to the command
        # line 20+ times until you get the BBIOx version string.

        self.send("\x0A" * 10)  # Send ENTER 10 times
        self.send("#\n")        # Send 'reset' command to the
                                # interactive terminal.
        self.flushInput();

        self.send("\x00" * 20)  # Send request to enter BitBang I/O mode.
        self.flushInput();

        # Wait for the bus pirate to process the request.
        self.wait()

        # Clear the input queue on the serial port.
        self.port.flushInput();

        # ...
        self.reset()

        bit_bang_io_mode_reply = self.recv(5)

        if bit_bang_io_mode_reply != self.__BIT_BANG_IO_MODE:
            raise BitBangIOException("Unable to enter BitBang I/O mode")

        self.setVersion(int(bit_bang_io_mode_reply[-1]))    # Version 1 is the
                                                            # only one at the
                                                            # moment.
        self.__init_ok = True

    def reset(self):
        """Send a reset command to the bus pirate."""
        self.send(self.__BBIO_CMD_RESET)
        # Wait for the bus pirate to process the request.
        self.wait()

    def __exitBitBangMode(self):
        """Reset Bus Pirate and return to user terminal."""
        self.reset()
        self.send(self.__BBIO_CMD_RESET_BP)

        self.wait()

        self.port.read(2000)
        self.port.flush()

    def wait(self, seconds=None):
        """Delay execution for a given number of seconds.  The argument may be
        a floating point number for subsecond precision."""

        # If not value was specified then use the default amount of time.
        if seconds is None:
            seconds = self.DEFAULT_WAIT_TIMEOUT_SECS

        # Perform wait operation.
        select([], [], [], seconds)

    #
    # General Commands for Higher-Level Modes.
    #
    def bulkTransfer(self, bulk_size):
        """Perform a bulk transfer using the currently selected bus on the Bus
        Pirate."""

        # Return a list of the bytes received.
        data = list()

        if bulk_size == 0:
            return data

        for bulk_round in range(0, bulk_size, 16):

            self.send((0b0001 << 4) | (bulk_size - 1))
            self.wait()
            if not self.recv():
                raise BitBangIOException(
                    "Unable to send bulk data round %d" % bulk_round)

            cur_bulk_size = 16 # FIXME

            for index in range(cur_bulk_size):
                byte    = self.recv(1, True)
                self.wait()
                result  = self.recv()

                if not byte or result is False:
                    raise BitBangIOException(
                        "Unable to receive bulk transfer for index %d." % index)

                data.append(byte)

        return data

    def send(self, data):
        """Send the specified data to the Bus Pirate."""
        # Convert to the appropriate type if needed because only strings can be
        # send and to facilitate the process of sendind numeric values to the
        # user avoiding previous transformation on this part it's done here.
        if self.__PERFORM_NUM_TO_STR_CONVERTION and type(data) in (int, float):
            data = chr(data)

        if self.__debug_traffic:
            print "--> %r" % data

        self.port.write(data)

    def recv(self, recv_count=1, return_data=False):
        """Receive the specified amount of bytes and return then if the user
        requested so."""
        # Read the raw data from the port comunicating with the bus pirate.
        # TODO: add support for redirection.
        data = self.port.read(recv_count)

        if recv_count == 1 and return_data == False:
            if data == chr(0x01):
                return True
            else:
                return False
        else:
            if self.__debug_traffic:
                print "<-- %r" % data
            return data

    def _wasCommandSuccessful(self):
        """Indicate if the last executed command was successfully carried out
        by checking if the value 1 was returned."""
        return self.recv()
