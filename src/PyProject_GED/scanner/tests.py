'''
Created on Aug 20, 2012

@author: spengler
'''


from django.test                                import TestCase
from PyProject_GED.scanner.core._imagescanner import ImageScanner



class Test(TestCase):
    
    def setUp(self):

        pass

    def tearDown(self):

        pass

    def testCriarTipoDeEvento(self):
        iscanner = ImageScanner()
        scanners = iscanner.list_scanners()
        self.assertEqual(True, len(scanners) > 0)