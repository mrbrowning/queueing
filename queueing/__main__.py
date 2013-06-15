"""
    queueing.__main__
    =================

    Run the simulation.

    :author: Michael Browning
    :copyright: (c) 2013 by Michael Browning.
    :license: BSD, see LICENSE for more details.
"""

import sys
import argparse
import Queue
import math

from .customer import Customer, CustomerSource
from .kiosk import Kiosk

def main(argv):
    parser = argparse.ArgumentParser(
        description='Simulate a grocery store self-checkout station.'
    )
    parser.add_argument('customers', type=int, help='the number of customers')
    parser.add_argument('lines', type=int, help='the number of lines')
    parser.add_argument('kiosks', type=int, help='the number of kiosks')
    args = parser.parse_args()

    if args.lines > args.kiosks:
        sys.stderr.write(
            'Error: The number of lines must be less than or equal to the '
            'number of kiosks.\n'
        )
        parser.print_help()
        sys.exit(1)

    lines = [Queue.Queue()] * args.lines
    customer_source = CustomerSource(args.customers, *lines)

    divisor = int(math.ceil(float(args.kiosks) / float(args.lines)))
    kiosks = [Kiosk(lines[i / divisor], i) for i in xrange(args.kiosks)]

    try:
        for k in kiosks:
            k.start()
        customer_source.start()
        customer_source.join(5)
    except (KeyboardInterrupt, SystemExit):
        sys.stderr.write('Quitting...\n')
        customer_source.stop()
        for k in kiosks:
            k.stop()

if __name__ == '__main__':
    main(sys.argv)
