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

#__revision__    = $Rev: 21 $
#__author__      = $Author: sebastianmuniz $
#__id__          = $Id$
#__date__        = $Date: 2010-08-23 01:02:20 -0300 (Mon, 23 Aug 2010) $
#__url__         = $URL$
__version__     = "1.0"

from sys                        import exit, stdout, stdin
from select                     import select
from optparse                   import OptionParser

from pyBusPirate2.UART          import *

def parse_prog_args():
    parser = OptionParser(usage="%prog [options] filename",
                                    version="%prog " + __version__)

    parser.set_defaults(command="read")

    parser.add_option("-v", "--verbose",
                        action="store_true", dest="verbose", default=True,
                        help="prints out more information")

    parser.add_option("-r", "--read",
                        action="store_const", dest="command", const="read",
                        help="read from SPI to file [default]")

    parser.add_option("-w", "--write",
                        action="store_const", dest="command", const="write",
                        help="write from file to SPI")

    parser.add_option("-i", "--interactive",
                        action="store_const", dest="command", const="interactive",
                        help="read/write to/from the UART")

    (options, args) = parser.parse_args()

    if options.command == "id":
        return (options, args)
    elif options.command != "interactive" and len(args) != 1:
        parser.print_help()
        #print options
        exit(1)
    else:
        return (options, args)

def interact(uart):
    """Interaction function, emulates a very dumb telnet client."""
    import thread
    thread.start_new_thread(listener, (uart,))

    while True:
        line = stdin.readline()
        if not line:
            break
        uart.send(line)

def listener(uart):
    """Helper for interact() -- this executes in the other thread."""
    while True:
        try:
            data = uart.recv(10)
        except EOFError:
            print '*** Connection closed by remote host ***'
            return
        if data:
            stdout.write(data)
        else:
            stdout.flush()

def main():
    """Interface the Bus Pirate with a UART-capable device."""

    # Read the command line parameters specified by the user.
    (opt, args)  = parse_prog_args()

    if not opt.command == "interactive":
        filename = args[0]
        if filename == "-":
            fd = stdout
        else:
            if opt.command == "read":
                fd = open(args[0], 'wb')
            elif opt.command == "write":
                fd = open(args[0], 'rb')

    # Create an instance of a UART bus handler using the Bus Pirate.
    print "[+] Initializing Bus Pirate to access a UART bus..."
    uart = Uart("/dev/ttyUSB0", 115200)

    # This step is optional (default is verbosity off)
    # Set verbosity level to print (or not) debugging information.
    print "[+] Setting verbosity to %s..." % opt.verbose
    uart.verbose(opt.verbose)

    # Set the appropriate baudrate for Bus Pirate to communicate with the
    # device using the UART bus.
    print "[+] Changing UART baudrate..."
    print "[+] UART baudrate was %s changed." % \
        ("successfully" if str(uart.setSpeed(UartSpeed._115200)) else "NOT")

    # Configure the UART bus to the correct xxx
    print "[+] Setting UART configuration..."
    print "[+] UART configuration was %s setted." % \
        ("successfully" if str(uart.setConfiguration(0, 0, 0, 0, 0)) else "NOT")

    # Check if the user requested to start reading the data received from the
    # UART bus and display it on the specified output media.
    if opt.command == "read":
        print "[+] Preparing to start receiving imput from UART..."
        print "[+] UART input state was %s setted." % \
            ("successfully" if str(uart.showInput(True)) else "NOT")

        print "[+] Reading from UART..."
        try:
            uart.enterBridgeMode()

            while True:
                fd.write(uart.recv(80, True))

        except KeyboardInterrupt:
            pass

        print "\n[+] Stopping UART input..."
        # Stop receiving input data from the UART bus.
        uart.showInput(False)

    elif opt.command == "write":
        print "[+] Writing to UART..."
        #uart.bulk_trans(4, [0xA, 0, 0, 0])
        #for i in range((int(opt.flash_size)/16)):
        #    uart.bulkTransfer(None)

    elif opt.command == "interactive":
        # Enter the interactive mode and let the user send and receive data to
        # and from the device.
        print "[+] Creating bridge between UART bus and device..."
        print "[+] Bridge between UART bus and device was %s created." % \
            (" successfully" if str(uart.enterBridgeMode()) else " NOT")

        print "[+] Entering interactive mode..."
        try:
            interact(uart)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
