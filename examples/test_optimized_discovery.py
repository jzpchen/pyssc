from pyssc import scan
import time

def test_discovery():
    print("Testing optimized discovery...")
    start_time = time.time()
    
    # Run discovery
    device_setup = scan()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Verify results
    if not device_setup or not device_setup.ssc_devices:
        print("❌ Test failed: No devices found")
        return False
        
    if len(device_setup.ssc_devices) != 2:
        print(f"❌ Test failed: Expected 2 devices, found {len(device_setup.ssc_devices)}")
        return False
        
    print(f"✅ Test passed! Found {len(device_setup.ssc_devices)} devices in {elapsed_time:.2f} seconds:")
    for device in device_setup.ssc_devices:
        print(f"  - {device.name} at {device.ip}")
        
    if elapsed_time > 1.0:
        print(f"⚠️ Warning: Discovery took longer than expected ({elapsed_time:.2f}s > 1.0s)")
    
    return True

if __name__ == "__main__":
    # First reinstall the package to ensure we're testing the latest changes
    import subprocess
    import sys
    import os
    
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print("Reinstalling package in development mode...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", project_root])
    
    # Run the test
    test_discovery()
