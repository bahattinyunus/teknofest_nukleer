import random

class ReactorCore:
    def __init__(self):
        self.temperature = 300.0  # Kelvin
        self.pressure = 100.0     # Bar
        self.radiation_level = 0.05 # mSv/h
        self.control_rod_status = "INSERTED"

    def boot_system(self):
        print("[CORE] Diagnostic check: PASSED")
        print("[CORE] Cooling pumps: ONLINE")
        self.control_rod_status = "RETRACTING"
        print("[CORE] Control rods: RETRACTING...")

    def monitor_loop(self):
        # Simulate slight fluctuations
        self.temperature += random.uniform(-1.5, 2.0)
        self.pressure += random.uniform(-0.5, 0.5)
        
        status = "NORMAL"
        if self.temperature > 350:
            status = "WARNING"
        
        print(f"| TEMP: {self.temperature:.2f}K | PRESS: {self.pressure:.2f} bar | RAD: {self.radiation_level} mSv/h | STATUS: {status}")

    def emergency_shutdown(self):
        print("\n\n🚨 SCRAM INITIATED 🚨")
        print("[SCRAM] Control rods fully inserted.")
        print("[SCRAM] Cooling max flow.")
        print("[SCRAM] Reactor shutting down safely.")
