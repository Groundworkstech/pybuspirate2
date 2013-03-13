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
# [-] Interactive console.

__version__ = "0.1"
__author__  = "Sebastian 'topo' Muniz"

from BitBang            import *

FOSC = (32000000/2)

class UartCfg:
    OUTPUT_TYPE = 0x10
    DATABITS    = 0x0C
    STOPBITS    = 0x02
    POLARITY    = 0x01

class UartSpeed:
    _300        = 0b0000
    _1200       = 0b0001
    _2400       = 0b0010
    _4800       = 0b0011
    _9600       = 0b0100
    _19200      = 0b0101
    _33250      = 0b0110
    _38400      = 0b0111
    _57600      = 0b1000
    _115200     = 0b1001

    SPEEDS = [  _300,
                _1200,
                _2400,
                _4800,
                _9600,
                _19200,
                _33250,
                _38400,
                _57600,
                _115200 ]

class UartException(BitBangIOException):
    """Standrd Uart class exception."""
    pass

"""
Binary UART mode command table

[+] 00000000 - Exit to bitbang mode, responds "BBIOx"
[+] 00000001 - Mode version string (ART1)
[+] 00000010 - Start echo UART RX
[+] 00000011 - Stop echo UART RX
[?] 00000111 - Manual baud rate config, send 2 bytes
[+] 00001111 - UART bridge mode (reset to exit)
[?] 0001xxxx - Bulk transfer, send 1-16 bytes (0=1byte!)
[+] 0100wxyz - Configure peripherals, w=power, x=pullups, y=AUX, z=CS
[+] 0110xxxx - Set speed (see options)
[+] 100wxxyz - Config:  w  = output type
                        xx = databits and parity
                        y  = stop bits
                        z  = RX polarity 
"""

class Uart(BitBangIO):
    """Provide access to the UART bus mode on the Bus Pirate."""

    __CMD_UART_START_ECHO_UART_RX           = 0b00000010
    __CMD_UART_STOP_ECHO_UART_RX            = 0b00000011
    __CMD_UART_SET_MANUAL_BAUDRATE_CONFIG   = 0b00000111
    __CMD_UART_ENTER_BRIDGE_MODE            = 0b00001111
    __CMD_UART_CONFIGURE_PERIPHERALS        = 0b01000000
    __CMD_UART_SET_BAUDRATE                 = 0b01100000
    __CMD_UART_SET_CONFIGURATION            = 0b10000000

    def __init__(self, port, speed):
        """Initialize the UART handler class."""
        # Initiate Bit Bang I/O mode
        BitBangIO.__init__(self, port, speed)

        # Instruct the Bus Pirate to interact with a device using the bus type
        # specified by the derived class.
        self.__setBusMode()

    def __setBusMode(self):
        """Select the UART bus mode to operate with the Bus Pirate."""
        self.send(BusMode.UART)
        self.wait()
        if not self.recv(4) == "ART1":
            raise UartException("Unable to set UART bus mode.")

    def setManualBaudrateConfig(self, baudrate):
        """Manually set the baud rate of the UART bus."""
        brg_value       = ((FOSC) / (4 * baudrate)) - 1
        brg_value_high  = ((brg_value >> 8) & 0xFF)
        brg_value_low   = (brg_value & 0xFF)

        self.send(self.__CMD_UART_SET_MANUAL_BAUDRATE_CONFIG)
        self.send(brg_value_high)
        self.send(brg_value_low)

        self.wait()

        return self.recv()

    def showInput(self, show_imput=True):
        """Show the incomming UART data or not according to the user specified
        settings."""
        if show_imput is True:
            self.send(self.__CMD_UART_START_ECHO_UART_RX)
        else:
            self.send(self.__CMD_UART_STOP_ECHO_UART_RX)

        # Return the answer which should always be True unless something went
        # wrong.
        return self.recv()

    def enterBridgeMode(self):
        """Create a bridge between the device connected to the UART bus on the
        Bus Pirate and the current terminal."""
        self.send(self.__CMD_UART_ENTER_BRIDGE_MODE)
        self.wait()
        return self.recv()

    def setConfiguration(self, output_type=0, databits=0, parity=0,
        stop_bits=0, rx_polarity=0):
        """Set the UART bus configuration to use for comunication."""
        # Parse the values and prepare the command with the following format:
        #
        # 100wxxyz - w  = output type
        #            xx = databits and parity
        #            y  = stop bits
        #            z  = RX polarity 
        #
        config  = self.__CMD_UART_SET_CONFIGURATION
        config |= (output_type  & 0b1) << 4
        config |= (databits     & 0b1) << 3
        config |= (parity       & 0b1) << 2
        config |= (stop_bits    & 0b1) << 1
        config |= (rx_polarity  & 0b1)

        self.send(config)
        self.wait()
        return self.recv()

    def configurePeripherals(self, power=0, pullups=0, aux=0, cs=0):
        """Set the cofiguration for each pin on the Bus Pirate."""
        # Parse the values and prepare the command with the following format:
        #
        # 0100wxyz w=power, x=pullups, y=AUX, z=CS
        #
        config  = self.__CMD_UART_CONFIGURE_PERIPHERALS
        config |= (power    & 0b1) << 3
        config |= (pullups  & 0b1) << 2
        config |= (aux      & 0b1) << 1
        config |= (cs       & 0b1)

        self.send(config)
        self.wait()
        return self.recv()

    def setSpeed(self, baudrate):
        """Set UART bus baudrate."""
        # Make sure that the user specified value is fine before doing
        # anything.
        if not self.isSupportedSpeed(baudrate):
            raise UartException("Invalid UART baudrate specified.")

        # Send the command and indicate to the user if it was successful
        # or not.
        self.send(self.__CMD_UART_SET_BAUDRATE | baudrate)
        self.wait()
        return self.recv()

    def isSupportedSpeed(self, speed):
        """Inidicate wheather or not the specifieds baud rate is valid."""
        return bool(speed in UartSpeed().SPEEDS)

