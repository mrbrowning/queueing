"""
    queueing.resources
    ==================

    Utilities and resources for queueing.

    :author: Michael Browning
    :copyright: (c) 2013 by Michael Browning.
    :license: BSD, see LICENSE for more details.
"""

import threading


class StoppableThread(threading.Thread):
    """A thread that exposes a stop command to halt execution."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()

    def stop(self):
        """Send the thread a stop request."""
        self._stop.set()

    def stopped(self):
        """Check if thread is stopped."""
        self._stop.isSet()
