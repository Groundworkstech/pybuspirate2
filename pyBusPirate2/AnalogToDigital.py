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

__all__     = [ "AnalogToDigitalConverter",
                "AnalogToDigitalConverterException"
                ]

class AnalogToDigitalConverterException(BitBangIOException):
    """Standard ADC class exception."""
    pass

class AnalogToDigitalConverter(BitBangIO):
    """Provide access to the ADC routines in the Bus Pirate."""

    # [+] 00010100 - Use ADC to convert read value.
    __BBIO_CMD_SETUP_ADC = 0x14 # 0b00010100

    def __init__(self, port, speed):
        """Initialize the Bus Pirate."""
        # Initiate Bit Bang I/O mode,
        BitBangIO.__init__(self, port, speed)

    def measure(self):
        """Measure the values obtained from the ADC."""
        #
        # ADC only available for v1, v2, v3
        #

        # Send the BitBang command and wait for the read value.
        self.send(self.__BBIO_CMD_SETUP_ADC)
        self.wait()

        raw_measure = self.recv(2, True)

        measure  = ord(raw_measure[0]) << 8
        measure |= ord(raw_measure[1])

        return measure

    def measureVolts(self):
        """Measure the volts on the ADC pin."""
        # Precalculated value for equal value resistor (/2)
        # ADC / 1024 * 3.3 * 2 = ADC / 155.1515
        return self.measure() / 155.1515
