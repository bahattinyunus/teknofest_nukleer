import sys
import time
from reactor_core import ReactorCore

def main():
    print("☢️  INITIALIZING NUCLEAR CONTROL SYSTEM ☢️")
    time.sleep(1)
    
    reactor = ReactorCore()
    reactor.boot_system()
    
    print("\n[SYSTEM] Monitoring active...")
    print("[SYSTEM] Press Ctrl+C to initiate emergency shutdown.")
    
    try:
        while True:
            reactor.monitor_loop()
            time.sleep(2)
    except KeyboardInterrupt:
        reactor.emergency_shutdown()

if __name__ == "__main__":
    main()
