'''
Created on Oct 5, 2012

@author: Shift IT | www.shiftit.com.br
'''

from django.db                  import models

import logging
import socket
import SocketServer
import json


class Servidor(models.Model):
    
    def iniciaSocket_UDP(self):
        try:
            UDP_IP="192.168.1.17"
            UDP_PORT=9999
            
            sock = socket.socket( socket.AF_INET, # Internet
                                  socket.SOCK_DGRAM ) # UDP
            sock.bind( (UDP_IP,UDP_PORT) )
            
            print '>>>>>>>>>>>>>>>>>>>>>>>>> PRONTO'
            
            while True:
                data, addr = sock.recvfrom( 1024 ) # buffer size is 1024 bytes
                print "[%s] Received Message: %s" % (addr, data)
                
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar os tipos de Indice: ' + str(e))
            return False
    
    def iniciaSocket_TCP(self):
        try:      
            TCP_IP="192.168.1.17"
            TCP_PORT=9999
                  
            # Create the server, binding to localhost on port 9999
            server = SocketServer.TCPServer((TCP_IP, TCP_PORT), MyTCPHandler)
        
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            print '>>>>>>>>>>>>>>>>>>>>>>>>> PRONTO'
            server.serve_forever()
                
        except Exception, e:
            logging.getLogger('PyProject_GED.controle').error('Nao foi possivel criar os tipos de Indice: ' + str(e))
            return False
        
class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        print 'Conectado'
        #self.request.sendall('conectado')
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        iMensagem= self.data
        print str(iMensagem).encode('UTF-8')
        print type(iMensagem)
        import simplejson
        parsed_data = simplejson.loads(iMensagem)
        #iJSON= json.loads(iMensagem)
        #print iJSON.index(u'usuario')
        print '---------------------------------------------'
        print 'USUARIO: %s' % parsed_data[0]['usuario']
        print 'SENHA: %s' % parsed_data[0]['senha']
        print '---------------------------------------------'
        
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())