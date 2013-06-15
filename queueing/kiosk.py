"""
    queueing.kiosk
    ==============

    Logic for checkout kiosks.

    :author: Michael Browning
    :copyright: (c) 2013 by Michael Browning.
    :license: BSD, see LICENSE for more details.
"""

import threading
import Queue


class Kiosk(threading.Thread):
    """A kiosk that customers check out at."""

    def __init__(self, line, kiosk_id=None):
        super(Kiosk, self).__init__()
        self.line = line
        self.id = kiosk_id
        self.daemon = True

    def run(self):
        while True:
            try:
                customer = self.line.get()
                print 'Customer %d at kiosk %d.' % (customer.id, self.id)
                customer.checkout()
            except Queue.Empty:
                pass
