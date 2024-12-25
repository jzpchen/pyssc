import time
from pyssc import scan

print("Starting discovery test...")
start_time = time.time()

# Run discovery
device_setup = scan(scan_time_seconds=1)  # Using default 1 second timeout

end_time = time.time()
elapsed_time = end_time - start_time

# Print results
print(f"\nDiscovery completed in {elapsed_time:.2f} seconds")
if device_setup and device_setup.ssc_devices:
    print(f"Found {len(device_setup.ssc_devices)} devices:")
    for device in device_setup.ssc_devices:
        print(f"  - {device.name} at {device.ip}")
else:
    print("No devices found")
