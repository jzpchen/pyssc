import time
from pyssc import scan
from pyssc.fast_scan import fast_scan

def test_scan(scan_func, name, **kwargs):
    print(f"\nTesting {name}...")
    start_time = time.time()
    device_setup = scan_func(**kwargs)
    elapsed_time = time.time() - start_time
    
    print(f"{name} completed in {elapsed_time:.2f} seconds")
    if device_setup and device_setup.ssc_devices:
        print(f"Found {len(device_setup.ssc_devices)} devices:")
        for device in device_setup.ssc_devices:
            print(f"  - {device.name} at {device.ip}")
    else:
        print("No devices found")
    return elapsed_time

# Test original scan
original_time = test_scan(scan, "Original scan", scan_time_seconds=1)

# Test optimized scan
optimized_time = test_scan(fast_scan, "Optimized scan", timeout=0.5)

print(f"\nSpeed improvement: {(original_time - optimized_time) / original_time * 100:.1f}%")
