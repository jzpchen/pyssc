import time
from zeroconf import IPVersion, ServiceBrowser, ServiceStateChange, Zeroconf
from .ssc_device import Ssc_device
from .ssc_device_setup import Ssc_device_setup
import threading

# Service type for SSC discovery
SSC_SERVICE_TYPE = '_ssc._tcp.local.'

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
            if info and info.type == SSC_SERVICE_TYPE:
                addresses = [addr for addr in info.parsed_addresses() if ':' in addr]
                if addresses:
                    name = name.replace('.' + SSC_SERVICE_TYPE, '')
                    self.found_devices.append(Ssc_device(name, addresses[0]))
                    if len(self.found_devices) >= 2:
                        self.device_setup = Ssc_device_setup(self.found_devices)
                        self.done_event.set()

def scan(scan_time_seconds=0.5) -> Ssc_device_setup:
    """
    Scan for SSC speakers on IPv6 network.
    Returns early if both speakers are found.
    
    Args:
        scan_time_seconds (float): Maximum time to wait for device discovery.
                                Default is 0.5 seconds.
        
    Returns:
        Ssc_device_setup: Setup object containing the found devices
    """
    scanner = Scanner()
    zeroconf = Zeroconf(ip_version=IPVersion.V6Only)
    browser = ServiceBrowser(zeroconf, SSC_SERVICE_TYPE,
                           handlers=[scanner.on_service_state_change])
    
    scanner.done_event.wait(scan_time_seconds)
    zeroconf.close()
    return scanner.device_setup or Ssc_device_setup(scanner.found_devices)
