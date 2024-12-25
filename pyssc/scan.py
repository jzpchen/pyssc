import time
from zeroconf import IPVersion, ServiceBrowser,\
                     ServiceStateChange, Zeroconf
from .ssc_device import Ssc_device
from .ssc_device_setup import Ssc_device_setup
import threading

class Scanner:
    def __init__(self):
        self.found_devices = []
        self.device_setup = None
        self.done_event = threading.Event()

    def on_service_state_change(self, zeroconf: Zeroconf,
                              service_type: str,
                              name: str,
                              state_change: ServiceStateChange) -> None:
        if state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            if info and info.type == '_ssc._tcp.local.':
                address = info.parsed_addresses()[0]
                name = info.name.replace('._ssc._tcp.local.', '')
                self.found_devices.append(Ssc_device(name, address))
                if len(self.found_devices) >= 2:  # We found both speakers
                    self.device_setup = Ssc_device_setup(self.found_devices)
                    self.done_event.set()

def scan(scan_time_seconds=0.5) -> Ssc_device_setup:
    """
    Fast speaker discovery optimized for a setup with 2 SSC speakers on IPv6.
    Returns early if both speakers are found.
    
    Args:
        scan_time_seconds (float): Maximum time to wait for device discovery in seconds.
                                Default is 0.5 seconds which is typically sufficient.
        
    Returns:
        Ssc_device_setup: Setup object containing the found devices
    """
    scanner = Scanner()
    zeroconf = Zeroconf(ip_version=IPVersion.V6Only)
    
    # Only browse for SSC service
    browser = ServiceBrowser(zeroconf, "_ssc._tcp.local.",
                           handlers=[scanner.on_service_state_change])
    
    # Wait until we either find both devices or timeout
    scanner.done_event.wait(scan_time_seconds)
    
    zeroconf.close()
    return scanner.device_setup or Ssc_device_setup(scanner.found_devices)
