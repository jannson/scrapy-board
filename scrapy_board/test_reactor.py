#!/usr/bin/env python

from twisted.internet import reactor, defer


def one(result):
    print "Start one()"
    for i in xrange(10000):
        print i
    print "End one()"
    reactor.stop()


def oneErrorHandler(failure):
    print failure
    print "INTERRUPTING one()"
    reactor.stop()    


if __name__ == '__main__':

    d = defer.Deferred()
    d.addCallback(one)
    d.addErrback(oneErrorHandler)
    reactor.callLater(1, d.callback, 'result')

    print "STARTING REACTOR..."
    try:
        reactor.run()
    except KeyboardInterrupt:
        print "Interrupted by keyboard. Exiting."
        reactor.stop()

