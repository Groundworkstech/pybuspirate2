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

__all__     = [ "SelfTest",
                "SelfTestException"
                ]

class SelfTestException(BitBangIOException):
    """Standard self-test class exception."""
    pass

class SelfTest(BitBangIO):
    """Provide access to the self-test routines in the Bus Pirate."""

    """
    [+] 00010000 - Short binary mode self-test
    [+] 00010001 - Long test (requires jumpers between +5 and Vpu, +3.3 and ADC)
    """
    __BBIO_CMD_SHORT_SELF_TEST      = 0x10 # 0b00010000
    __BBIO_CMD_LONG_SELF_TEST       = 0x11 # 0b00010001

    def __init__(self, port, speed):
        """Initialize the Bus Pirate."""
        # Initiate Bit Bang I/O mode
        BitBangIO.__init__(self, port, speed)

        self.setErrorsOnTest(0)

    def performShortSelftest(self):
        """Perform a quick self-test on the Bus Pirate that verifies the
        function of pins and peripherals (No jumpers set required)."""
        # Make sure that the command was completed enteirely by checking it
        # returned True but notice that it doesn't mean that errors didn't
        # happen during the test.
        if not self.__performSelfTest(self.__BBIO_CMD_SHORT_SELF_TEST):
            raise SelfTestException("Non successful return value form test")

        # Indicate if something wrong was detected during the test.
        return bool(self.getErrorsOnTest() == 0)

    def performLongSelftest(self):
        """Perform a more in depth self-test on the Bus Pirate that verifies
        the function of pins and peripherals (It requires jumpers between +5
        and Vpu, +3.3 and ADC)."""
        # Make sure that the command was completed enteirely by checking it
        # returned True but notice that it doesn't mean that errors didn't
        # happen during the test.
        if not self.__performSelfTest(self.__BBIO_CMD_LONG_SELF_TEST):
            raise SelfTestException("Non successful return value form test")

        # Indicate if something wrong was detected during the test.
        return bool(self.getErrorsOnTest() == 0)

    def __performSelfTest(self, test_type):
        """Send the appropriate self-test request to the Bus Pirate and store
        the results."""
        # Send the command indicating the test requested (either short or long
        # self-test).
        self.send(test_type)
        self.wait()

        # Receive the number of errors happened during the tests.
        self.setErrorsOnTest(ord(self.recv(1, True)))

        # Send the signal to the firmware to stop echoing characters and leave
        # the self-test routine to go back to normal operation.
        self.send(0xff)

        # Return a boolean indicating if the command was carried successfully
        # (doesn't mean errors didn't occur).
        return self.recv()

    def setErrorsOnTest(self, errors_number):
        """Store the number of errors that happened during the last self-test
        executed."""
        self.self_test_errors = errors_number

    def getErrorsOnTest(self):
        """Return the number of errors that happened during the last self-test
        executed or None if no self-test has been executed yet."""
        return self.self_test_errors

