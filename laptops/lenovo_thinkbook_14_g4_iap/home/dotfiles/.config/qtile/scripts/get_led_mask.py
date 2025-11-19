"""
The work of this solution based on parsing LED mask: 00000000. Run the script to detect
which bits responsible for switching layouts in your system, just run it and switching.

"""

#!/usr/bin/env python3

import subprocess
import time

def monitor_led_changes():
    print("Monitoring changes of LED mask...")
    print("Switch keyboard layouts and watch changes")
    print("Press Ctrl+C to exit")
    
    last_mask = None
    
    try:
        while True:
            result = subprocess.run(['xset', '-q'], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'LED mask:' in line:
                        led_hex = line.split('LED mask:')[-1].strip()
                        led_mask = int(led_hex, 16)
                        
                        if last_mask is not None and led_mask != last_mask:
                            print(f"LED mask changed: {last_mask:08x} -> {led_mask:08x}")
                            print(f"Changed bits: {last_mask ^ led_mask:08x}")
                            
                            changed_bits = last_mask ^ led_mask
                            for bit in range(0, 32):
                                if changed_bits & (1 << bit):
                                    print(f"  Bit {bit} (0x{1 << bit:08x}) changed")
                            
                            print("-" * 40)
                        
                        last_mask = led_mask
                        break
            
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStop monitoring")

if __name__ == "__main__":
    monitor_led_changes()
