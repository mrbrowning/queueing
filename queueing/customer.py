"""
    queueing.customer
    =================

    Logic for customers and customer spawning.

    :author: Michael Browning
    :copyright: (c) 2013 by Michael Browning.
    :license: BSD, see LICENSE for more details.
"""

import random
import time
import threading

from .resources import StoppableThread


MIN_CHECKOUT_DURATION = 60
MAX_CHECKOUT_DURATION = 360

MIN_ENQUEUE_DURATION = 5
MAX_ENQUEUE_DURATION = 45


class Customer(object):
    """A customer, who takes a certain time to check out."""

    def __init__(
            self, customer_source, customer_id=None, checkout_duration=None):
        self.customer_source = customer_source
        self.id = customer_id if customer_id is not None else (
            random.randint(0, self.customer_source.num_customers)
        )
        self.checkout_duration = (
            checkout_duration if checkout_duration is not None else (
                random.randint(MIN_CHECKOUT_DURATION, MAX_CHECKOUT_DURATION)
            )
        )

    def checkout(self):
        """Simulate checking out by blocking for a duration equal to
        `self.checkout_duration` milliseconds."""
        time.sleep(float(self.checkout_duration) / 1000.0)
        self.customer_source.increment_served()
        print 'Customer %d checked out (%d ms).' % (
            self.id, self.checkout_duration
        )


class CustomerSource(StoppableThread):
    """A customer source that generates customers at random intervals."""

    def __init__(self, num_customers, *lines):
        super(CustomerSource, self).__init__()
        self.num_customers = num_customers
        self.lines = lines
        self.created = 0
        self.served = 0
        self.lock = threading.Lock()

    def run(self):
        """Add customers to the shortest line until `self.num_customers`
        customers have been created.
        """
        while self.created < self.num_customers and not self._stop.isSet():
            min(self.lines, key=lambda x: x.qsize()).put(Customer(self, self.created))
            self.created += 1
            time.sleep(
                random.randint(MIN_ENQUEUE_DURATION, MAX_ENQUEUE_DURATION) /
                1000.0
            )

        # We want this thread to live until all customers have been served.
        # That way, the other threads can be daemon threads and the program can
        # exit when this thread completes.
        while self.served < self.num_customers and not self._stop.isSet():
            pass

    def increment_served(self):
        """Increment the number of customers served thread-safely."""
        self.lock.acquire()
        self.served += 1
        self.lock.release()
