import time
import threading
from pyssc.tracker import Tracker
import sys

def device_callback(device_setup):
    """Callback function that prints the current state of devices"""
    print("\nDevices changed! Current devices:")
    for device in device_setup.ssc_devices:
        print(f"- {device.name} at {device.ip}")

def main():
    # Create and start the tracker
    tracker = Tracker()
    tracker.register_callback(device_callback)
    
    print("Starting SSC device tracking...")
    tracker.start()

    try:
        # Keep the tracker running for 30 seconds
        print("Tracking for 30 seconds. Connect/disconnect SSC devices to see updates...")
        time.sleep(30)
    except KeyboardInterrupt:
        print("\nTracking interrupted by user")
    finally:
        print("\nStopping tracker...")
        tracker.stop()
        print("Tracker stopped.")

if __name__ == "__main__":
    main()
