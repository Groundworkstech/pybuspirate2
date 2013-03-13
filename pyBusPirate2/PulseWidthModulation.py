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

__version__ = "0.1"
__author__  = "Sebastian 'topo' Muniz"

from BitBang            import *

__all__     = [ "PulseWidthModulation",
                "PulseWidthModulationException"
                ]

class PulseWidthModulationException(BitBangIOException):
    """Standard PWM class exception."""
    pass

class PulseWidthModulation(BitBangIO):
    """Provide access to the PWM routines in the Bus Pirate."""

    """
    [-] 00010010 - Setup pulse-width modulation (requires 5 byte setup)
    [-] 00010011 - Clear/disable PWM
    """
    __BBIO_CMD_SETUP_PWM    = 0x12 # 0b00010010
    __BBIO_CMD_CLEAR_PWM    = 0x13 # 0b00010011

    def __init__(self, port, speed):
        """Initialize the Bus Pirate."""
        # Initiate Bit Bang I/O mode,
        BitBangIO.__init__(self, port, speed)

    def setup(self, prescaler, dutycycle, period):
        """..."""
        # TODO: Untested

        # Send the BitBang command to clear PWD and wait until it's executed.
        self.send(self.__BBIO_CMD_SETUP_PWM)

        # Transmite prescalar but first make sure only the 2 lower bits are
        # used.
        self.send(prescaler & 0x3)

        # Transmit 16 bits indicating the duty cycle.
        self.send((dutycycle >> 8) & 0xFF)
        self.send(dutycycle & 0xFF)

        # Transmit the 16 bits period value.
        self.send((period >> 8) & 0xFF)
        self.send(period & 0xFF)

        self.wait()

        # This command should always return 1.
        return self._wasCommandSuccessful()

    def clear(self):
        """Remove the PWM settings and return to normal."""

        # Send the BitBang command to clear PWD and wait until it's executed.
        self.send(self.__BBIO_CMD_CLEAR_PWM)
        self.wait()

        # This command should always return 1.
        return self._wasCommandSuccessful()
