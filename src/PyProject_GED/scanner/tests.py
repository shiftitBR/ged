'''
Created on Aug 20, 2012

@author: spengler
'''


from django.test                                import TestCase
from PyProject_GED.scanner.core._imagescanner import ImageScanner
import socket



class Test(TestCase):
    
    def setUp(self):
        self.mokarClient()

        pass

    def tearDown(self):

        pass

    #def testCriarTipoDeEvento(self):
    #    iscanner = ImageScanner()
    #    scanners = iscanner.list_scanners()
    #    self.assertEqual(True, len(scanners) > 0)
    
    def testClient(self):
        UDP_IP="127.0.0.1"
        UDP_PORT=5005
        
        sock = socket.socket( socket.AF_INET, # Internet
                              socket.SOCK_DGRAM ) # UDP
        sock.bind( (UDP_IP,UDP_PORT) )
        
        while True:
            data, addr = sock.recvfrom( 1024 ) # buffer size is 1024 bytes
            print "received message:", data
    
    def mokarClient(self):

        UDP_IP="127.0.0.1"
        UDP_PORT=5005
        MESSAGE="Hello, World!"
        
        print "UDP target IP:", UDP_IP
        print "UDP target port:", UDP_PORT
        print "message:", MESSAGE
        
        sock = socket.socket( socket.AF_INET, # Internet
                              socket.SOCK_DGRAM ) # UDP
        sock.sendto( MESSAGE, (UDP_IP, UDP_PORT) )