from zeroconf import IPVersion, ServiceBrowser, ServiceStateChange, Zeroconf
from .ssc_device import Ssc_device
from .ssc_device_setup import Ssc_device_setup
import threading
from typing import Callable, Optional
import logging

# Service type for SSC discovery
SSC_SERVICE_TYPE = '_ssc._tcp.local.'

class Tracker:
    """
    A continuous tracker for SSC devices that monitors additions and removals.
    Notifies registered callbacks when device changes occur.
    """
    def __init__(self):
        self.device_setup = Ssc_device_setup()
        self.zeroconf = None
        self._callback: Optional[Callable[[Ssc_device_setup], None]] = None
        self._browser = None
        self._running = False
        self._lock = threading.Lock()

    def on_service_state_change(self,
                              zeroconf: Zeroconf,
                              service_type: str,
                              name: str,
                              state_change: ServiceStateChange) -> None:
        """Handle service state changes from zeroconf."""
        if not self._running or service_type != SSC_SERVICE_TYPE:
            return

        with self._lock:
            if state_change is ServiceStateChange.Added:
                info = zeroconf.get_service_info(service_type, name)
                if info and info.type == SSC_SERVICE_TYPE:
                    # Get first IPv6 address if available
                    addresses = [addr for addr in info.parsed_addresses() if ':' in addr]
                    if addresses:
                        device_name = name.replace('.' + SSC_SERVICE_TYPE, '')
                        device = Ssc_device(device_name, addresses[0])
                        self.device_setup.add_device(device)
                        if self._callback:
                            self._callback(self.device_setup)

            elif state_change is ServiceStateChange.Removed:
                device_name = name.replace('.' + SSC_SERVICE_TYPE, '')
                for device in self.device_setup.ssc_devices:
                    if device.name == device_name:
                        self.device_setup.remove_device(device)
                        if self._callback:
                            self._callback(self.device_setup)
                        break

    def register_callback(self, callback: Callable[[Ssc_device_setup], None]) -> None:
        """Register a callback function to be notified of device changes."""
        self._callback = callback

    def start(self) -> None:
        """Start tracking SSC devices."""
        if not self._running:
            self._running = True
            self.zeroconf = Zeroconf(ip_version=IPVersion.V6Only)
            self._browser = ServiceBrowser(
                self.zeroconf,
                SSC_SERVICE_TYPE,
                handlers=[self.on_service_state_change]
            )

    def stop(self) -> None:
        """Stop tracking and clean up resources."""
        self._running = False
        if self._browser:
            self._browser.cancel()
        if self.zeroconf:
            self.zeroconf.close()
            self.zeroconf = None

    @property
    def devices(self) -> Ssc_device_setup:
        """Get the current set of found devices."""
        return self.device_setup
