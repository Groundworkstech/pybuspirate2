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

__author__      = "Sebastian 'topo' Muniz"
__version__     = "1.0"

from sys                        import exit
from optparse                   import OptionParser

from pyBusPirate2.SelfTest      import SelfTest, SelfTestException

def parse_prog_args():
    parser = OptionParser(usage="%prog bp_port [options]",
                                    version="%prog " + __version__)

    parser.set_defaults(command="read")

    parser.add_option("-v", "--verbose",
                        action="store_true", dest="verbose", default=True,
                        help="prints out more information")

    parser.add_option("-l", "--long",
                        action="store_const", dest="short_self_test",
                        const=False, help="Perform a full self-test" \
                        " (requieres pins connections)")

    parser.add_option("-s", "--short",
                        action="store_const", dest="short_self_test",
                        const=True, help="Perform a short self-test")

    (options, args) = parser.parse_args()

    if options.short_self_test is None:
        parser.print_help()
        #print options
        exit(1)

    return (options, args)

def main():
    """Initialize the Bus Pirate and execute the selected self-test."""

    # Read the command line parameters specified by the user.
    (opt, args)  = parse_prog_args()

    try:
        # Create the connection to the Bus Pirate.
        print "[+] Connecting to the Bus Pirate and initiating BitBang mode..."

        bp = SelfTest("/dev/ttyUSB0", 115200)
        print "[+] Successfully connected to the Bus Pirate."

        # This step is optional (default is verbosity off)
        # Set verbosity level to print (or not) debugging information.
        print "[+] Setting verbosity to %s..." % opt.verbose
        bp.verbose(opt.verbose)

        if opt.short_self_test:
            # Invoke the SHORT self-test.
            print "[+] Performing short self-test..."
            self_test = bp.performShortSelftest()
        else:
            # Invoke the LONG self-test but before starting let the user
            # perform the pins connections.
            print "[!]", "*" * 50
            print "[!] Please remove any external device."
            print "[!] Please connect the pins appropriately."
            print "[!]", "*" * 50
            raw_input("[+] Press any key to continue...")
            print "[+] Performing long self-test..."

            self_test = bp.performLongSelftest()

        # Display the number of errors in the test, if any.
        if self_test:
            print "[+] Bus Pirate self-test was successful."
        else:
            print "[-] Bus Pirate self-test indicated %d errors." % \
                bp.getErrorsOnTest()

    except SelfTestException, err:
        print "[-] Exception: %s" % err

if __name__ == "__main__":
    main()
