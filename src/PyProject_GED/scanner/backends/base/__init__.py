"""Abstract base classes

$Id$"""

class ScannerManager(object):
    """Abstract ScannerManager class"""

    def __init__(self, **kwargs):
        self._devices = []
    
    def _refresh(self):
        """Look for new scanner devices"""
        raise NotImplementedError

    def get_scanner(self, scanner_id=None, scanner_device=None):
        """Return a scanner with the given ID, device string, or None if not found"""
        devices = self.list_scanners()

        for dev in devices:
            if dev.id == scanner_id or dev._device == scanner_device:
                return dev
        return None

    def list_scanners(self, *args, **kwargs):
        """Return a list with all the available devices"""
        self._refresh(*args, **kwargs)
        return self._devices      

class Scanner(object):
    """Abstract Scanner class.

    In adition to the methods the classes extending this class must also
    have the following attributes:
    
        id: unique identifier for the device on the current machine
        name: device name
        manufacturer: device manufacturer
        description: device description

    Usually all this attributes can be accessed directly on the device. 

    """

    def scan(self, dpi=200):
        """Scan a new image using the given DPI and returns a PIL object"""
        raise NotImplementedError

    def status(self):
        """Get device status"""
        # TODO: Define standard status
        raise NotImplementedError
