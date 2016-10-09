#!/usr/bin/env python2
"""
SC-Controller - Poller

Uses select to pool for file descriptors. Driver classes can use
daemon.get_poller().register and .unregister to add file descriptors and
register callbacks to be called when data is available in them.

Callback is called as callback(fd, event) where event is one of select.POLL*
"""
import select, logging
log = logging.getLogger("Poller")

class Poller(object):
	POLLIN = select.POLLIN
	POLLOUT = select.POLLOUT
	POLLPRI = select.POLLPRI
	
	def __init__(self):
		self._events = {}
		self._callbacks = {}
		self._pool_in = ()
		self._pool_out = ()
		self._pool_pri = ()
	
	
	def register(self, fd, events, callback):
		self._events[fd] = events
		self._callbacks[fd] = callback
		self._generate_lists()
	
	
	def unregister(self, fd):
		self._fd_dict.pop(fd)
		self._generate_lists()
	
	
	def _generate_lists(self):
		self._pool_in = [ fd for fd, events in self._events.iteritems() if events & Poller.POLLIN ]
		self._pool_out = [ fd for fd, events in self._events.iteritems() if events & Poller.POLLOUT ]
		self._pool_pri = [ fd for fd, events in self._events.iteritems() if events & Poller.POLLPRI ]
	
	
	def poll(self, timeout=1):
		inn, out, pri = select.select( self._pool_in, self._pool_out, self._pool_pri, timeout )
		
		for fd in inn:
			self._callbacks[fd](fd, Poller.POLLIN)
		for fd in out:
			self._callbacks[fd](fd, Poller.POLLOUT)
		for fd in pri:
			self._callbacks[fd](fd, Poller.POLLPRI)
