#!/usr/bin/env python
# encoding: utf-8
"""
This file is part of pyBusPirate2
Download at http://code.google.com/p/pybuspirate2/

Copyright (c) 2010 Sebastian Muniz <sebastianmuniz@gmail.com>

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

__author__  = "Sebastian 'topo' Muniz"
__version__     = "1.0"

from sys                            import exit, stdout
from optparse                       import OptionParser

from pyBusPirate2.AnalogToDigital   import *

def parse_prog_args():
    parser = OptionParser(usage="%prog [options] <bus pirate port>",
                                    version="%prog " + __version__)

    parser.set_defaults(command="read")

    parser.add_option("-v", "--verbose",
                        action="store_true", dest="verbose", default=False,
                        help="prints out more information")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        exit()

    return (options, args[0])

def main():
    """Interface the Bus Pirate with the Analog to Digital Converter to measure
    voltage."""

    # Read the command line parameters specified by the user.
    (opt, dev)  = parse_prog_args()

    # Create an instance of ADC converter using the Bus Pirate.
    print "[+] Initializing Bus Pirate to access the A/D converter..."
    adc = AnalogToDigitalConverter(dev, 115200)

    # This step is optional (default is verbosity off)
    # Set verbosity level to print (or not) debugging information.
    print "[+] Setting verbosity to %s..." % opt.verbose
    adc.verbose(opt.verbose)

    try:
        while True:
            # Measute the vols on ADC pin until the user presses CTRL-C
            stdout.write("\r[+] Volts : %.2f" % adc.measureVolts())
            stdout.flush()

    except KeyboardInterrupt:
        pass

    print "\n[+] Exiting..."

if __name__ == "__main__":
    main()
