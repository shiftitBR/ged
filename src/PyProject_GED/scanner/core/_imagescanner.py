"""Imagescanner main class. All embeded backends are loaded here.

$Id$""" 

import os
import platform
import logging
from importlib import import_module

from PyProject_GED.scanner import settings


OSX_BACKEND = 'PyProject_GED.scanner.backends.osx'
POSIX_BACKEND = 'PyProject_GED.scanner.backends.sane'
NT_BACKEND = 'PyProject_GED.scanner.backends.twain'
NETWORK_BACKEND = 'PyProject_GED.scanner.backends.net'
TEST_BACKEND = 'PyProject_GED.scanner.backends.test'

# Look for aditional backends
BACKENDS = getattr(settings, 'BACKENDS', None)


class ImageScanner(object):
    """Implements the interface from the backends with the lib."""

    def __init__(self, **kwargs):
        """Load the appropriate backends and its scanner managers.
    
        All keyword arguments are also passed to the constructor
        of each one of the ScannerManager.

        """
        logging.debug('[_imagescanner 33] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> init 1') 
        self.managers = []
        backends = []

        # Enable default backend for each system
        if os.name == 'posix':
            if platform.system() == 'Darwin':
                logging.debug('OSX backend enabled (%s)', OSX_BACKEND)
                backends.append(OSX_BACKEND)
            else: 
                logging.debug('Posix backend enabled (%s)', POSIX_BACKEND)
                backends.append(POSIX_BACKEND)

        elif os.name == 'nt':
            logging.debug('NT backend enabled (%s)', NT_BACKEND)
            backends.append(NT_BACKEND)
        
        logging.debug('[_imagescanner 50] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> init 2')
        
        # Check if we should load the test backend
        if getattr(settings, 'ENABLE_TEST_BACKEND', False):
            logging.debug('Test backend enabled (%s)', TEST_BACKEND)
            backends.append(TEST_BACKEND)
        
        # Check if we should enable net backend
        if getattr(settings, 'ENABLE_NET_BACKEND', False):
            logging.debug('Network backend enabled (%s)', NETWORK_BACKEND)
            backends.append(NETWORK_BACKEND)

        # Check if the user has own backends defined
        if BACKENDS is not None:
            logging.debug('Adding user backends (%s)', BACKENDS)
            backends.extend(BACKENDS)
        
        for backend in backends:    
            try:
                logging.debug('Importing %s', backend)
                backend_module = import_module(backend)
            except Exception, exc:
                logging.warning('Error importing %s [skiping]', backend)
                logging.warning(exc)
                # Could not import, so go to the next backend 
                continue

            try:
                manager = backend_module.ScannerManager(**kwargs)
                logging.debug('[_imagescanner 79] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> init 3')
            except AttributeError:
                logging.error('Backend %s does not implement '
                              'ScannerManager class [skiping]', backend)
                # Backend not implement the required API, so skip it
                continue 
        
            logging.debug('[_imagescanner 85] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> init 4')
            self.managers.append(manager)
            logging.debug('[_imagescanner 88] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> init 5')

    def list_scanners(self, *args, **kwargs):
        """List all devices for all the backends available"""
        logging.debug('[_imagescanner 86] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> list_scanners 1') 
        logging.debug('Looking for all scanner devices') 
        scanners = []
        for manager in self.managers:
            scanners.extend(manager.list_scanners(*args, **kwargs))
       
        logging.debug('Found scanners: %s', scanners) 
        return scanners

    def get_scanner(self, scanner_id=None, scanner_device=None):
        """Get the device with the given ID"""
        if scanner_id:
            logging.debug('Looking for scanner with id: %s' % scanner_id)
        elif scanner_device:
            logging.debug('Looking for scanner with device: %s' % scanner_device)
        scanner = None
        for manager in self.managers:
            scanner = manager.get_scanner(scanner_id, scanner_device)
            if scanner is not None:
                if scanner_id:
                    logging.debug('Scanner %s found', scanner_id)
                elif scanner_device:
                    logging.debug('Scanner %s found', scanner_device)
                return scanner
        if scanner_id:
            logging.debug('Scanner %s not found', scanner_id)
        elif scanner_device:
            logging.debug('Scanner %s not found', scanner_device)

    def scan(self, scanner_id, **kwargs):
        """Shortcut for scanning without get the device"""
        logging.debug('Trying to scan using: %s and %s', scanner_id, kwargs)
        scanner = self.get_scanner(scanner_id)
        if scanner is not None:
            return scanner.scan(**kwargs)
       
        logging.info('Scan failed. Scanner %s not found', scanner_id)
