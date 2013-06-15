queueing
========

I was at my local grocery store and was wondering about a particular policy they
enforce at the self-checkout kiosks. There are two rows with two adjacent kiosks
each, and they ask that customers line up separately for each row rather than
forming one large line that feeds all four kiosks. My guess is that they do this
to prevent a single large line from spiraling outwards into the shelves and
blocking customer traffic, but I was curious as to whether this arrangement has
any effect on the total time to serve a given number of customers or the average
time to serve a customer from the point of enqueueing to the point of leaving
the kiosk or the variance on that time or any number of other factors.

Right now I haven't implemented any of the analysis logic, but the basic
mechanism of the simulation is there. Customers are assigned a random checkout
duration in milliseconds when they're spawned by a global customer source
thread, which sends every new customer to the shortest line. Lines feed into
kiosk threads, where the customer checks out for an amount of time equal to
their checkout duration. The number of lines is equal to or less than the number
of kiosks.

Some things I'm thinking about as I proceed: should customers be able to switch
to a line that becomes shorter than the one they're waiting on? Should checkout
time be modeled based on number of items rather just assigning a random
duration? If so, should checkout time include a fixed base checkout duration on
top of which the time per item durations are added? Do any of those improve the
model with respect to the phenomenon of interest?

Finally, I'm aware that queueing theory probably has something to say about
this, but the only result from that particular branch of mathematics that I'm
familiar with is Little's Law, and this seemed like a fun project for a Saturday
morning.

Quick start
-----------

Run queueing:

    python -m queueing -h
    usage: __main__.py [-h] customers lines kiosks
    
    Simulate a grocery store self-checkout station.
    
    positional arguments:
      customers   the number of customers
      lines       the number of lines
      kiosks      the number of kiosks
    
    optional arguments:
      -h, --help  show this help message and exit
