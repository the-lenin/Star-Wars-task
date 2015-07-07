#!/usr/bin/python
#encoding: utf-8

import sys
import time
import socket
import asyncore
import exceptions

from socket import AF_INET, SOCK_STREAM
from asyncore import dispatcher
from threading import Thread, RLock

class PiCalcThread(Thread):
    def __init__(self, buffer, lock):
        Thread.__init__(self)
        self.buffer = buffer
        self.lock = lock
        
    def run(self):
        """ See http://web.comlab.ox.ac.uk/oucl/work/jeremy.gibbons/publications/spigot.pdf """
        q,r,t,k,n,l = 1,0,1,1,3,3
        
        while True:
            if 4*q+r-t < n*t:
                self.lock.acquire()
                self.buffer.newDigits(str(n))
                self.lock.release()
                
                q,r,t,k,n,l = (10*q,10*(r-n*t),t,k,(10*(3*q+r))/t-10*n,l)
            else:
                q,r,t,k,n,l = (q*k,(2*q+r)*l,t*l,k+1,(q*(7*k+2)+r*l)/(t*l),l+2)
            
            time.sleep(0.001)

class PiGenerator(list):
    def __init__(self):
        list.__init__(self)
        self.calculator = None
        self.lock = RLock()
        self.digits = ''
    
    def subscribe(self, obj):  
        self.lock.acquire()
        try:     
            self.append(obj)
            self._notify(obj=obj)
        finally:
            self.lock.release()            
            
        if not self.calculator:
            self.calculator = PiCalcThread(self, self.lock)
            self.calculator.start()
        else:
            if len(self) > 0:
                self._resumeCalculator()
                
    def unsubscribe(self, obj):
        self.lock.acquire()
        self.remove(obj)   
        self.lock.release()
             
        if len(self) <= 0:
            self._pauseCalulator()
            
    def _pauseCalulator(self):
        self.lock.acquire()
    
    def _resumeCalculator(self):
        try: self.lock.release()
        except exceptions.AssertionError: pass
            
    def _notify(self, digits = None, obj = None):
        objs = [obj] if obj else self
        digits = digits or self.digits
        
        for obj in objs:
            obj.update(digits)
        
    def newDigits(self, digits):
        self.digits += digits
        self._notify(digits)
        
class Stream(object):
    def __init__(self, generator):
        object.__init__(self)
        self.data = ''
        self.generator = generator
        self.closed = False
        
        generator.subscribe(self)
        
    def update(self, data):
        self.data += data
        
    def read(self):
        if self.closed: return None
        data = self.data
        self.data = ''
        return data
        
    def close(self):
        self.generator.unsubscribe(self)
        self.closed = True
        self.data = ''

class Server(dispatcher, dict):
    writable = lambda x: False
    
    def __init__(self, host = None, port = 0xB00B):
        dispatcher.__init__(self)
        
        self.create_socket(AF_INET, SOCK_STREAM)
        dict.__init__(self, {self.fileno(): self})
        
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(0xA)
        
        self.dataSource = PiGenerator()
        
    def removeClient(self, client):
        del self[client.fileno()]
        
    def handle_accept(self):
        sock, (host, port) = self.accept()
        print 'new client from %s:%d' % (host, port)
        
        stream = Stream(self.dataSource)        
        self[sock.fileno()] = Client(sock, self, stream)
        
    def handle_error(self):
        print 'Server error: %s' % sys.exc_value
        sys.exit(1)
    
class Client(dispatcher):
    readable = lambda x: False    
    
    def __init__(self, sock, server, stream):
        dispatcher.__init__(self, sock)
        self.server = server
        self.stream = stream
        self.buffer = ''
        
    def handle_error(self):
        print 'Client error: %s' % sys.exc_value
        import traceback
        print traceback.format_exc(1000)
        sys.exit(1)        
        
    def handle_write(self):                
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]
        
    def handle_expt(self):
        print 'client dropped connection'        
        self.close()

    def handle_close(self):
        pass
        
    def close(self):
        self.server.removeClient(self)
        self.stream.close()
        self.buffer = ''
        dispatcher.close(self)
        
    def writable(self):
        data = self.stream.read()
        if data == None:
            print 'client finished reading'
            self.close()
            return False
        
        self.buffer += data
        return len(self.buffer) > 0

def main():
    try:
        asyncore.loop(0.1, True, Server('127.0.0.1'))
    except KeyboardInterrupt:
        print '\nBye :-*'
        sys.exit(0)

if __name__ == '__main__':
    main()
    
