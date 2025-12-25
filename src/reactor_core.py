import random
import json
import os
import logging

class ReactorCore:
    def __init__(self, config_path="config.json"):
        self.load_config(config_path)
        
        # State Variables
        self.temperature = self.config["initial_state"]["temperature"]
        self.pressure = self.config["initial_state"]["pressure"]
        self.neutron_flux = self.config["initial_state"]["neutron_flux"]
        self.control_rod_pos = self.config["initial_state"]["control_rod_pos"] # 0=In, 100=Out
        self.coolant_flow = 50.0 # Percentage
        self.scram_active = False
        self.power_mw = 0.0
        
        # Setup Logger
        if not os.path.exists("logs"):
            os.makedirs("logs")
        
        logging.basicConfig(
            filename="logs/reactor.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def load_config(self, path):
        if os.path.exists(path):
            with open(path, "r") as f:
                self.config = json.load(f)
        else:
            # Fallback defaults
            self.config = {
                "initial_state": {"temperature": 300, "pressure": 100, "neutron_flux": 1e8, "control_rod_pos": 0},
                "thresholds": {"max_temp": 600, "critical_temp": 850, "max_pressure": 150}
            }

    def update_control_rods(self, position):
        self.control_rod_pos = max(0, min(100, position))
        self.logger.info(f"Control rods adjusted to {self.control_rod_pos}%")

    def update_coolant_flow(self, flow):
        self.coolant_flow = max(0, min(100, flow))
        self.logger.info(f"Coolant flow adjusted to {self.coolant_flow}%")

    def step(self):
        """Simulate one time step of reactor physics."""
        if self.scram_active:
            self.control_rod_pos = 0
            self.coolant_flow = 100
            
        # 1. Neutron Flux calculation (simplified)
        # Exposure of rods increases flux
        flux_delta = (self.control_rod_pos - 50) * 1e6
        self.neutron_flux = max(1e6, self.neutron_flux + flux_delta + random.uniform(-1e5, 1e5))
        
        # 2. Power calculation
        self.power_mw = self.neutron_flux / 1e9 * 10 
        
        # 3. Heat accumulation vs Cooling
        heat_gen = self.power_mw * 2.5
        heat_removal = (self.coolant_flow / 100.0) * 5.0 * (self.temperature / 300.0)
        
        self.temperature += (heat_gen - heat_removal) + random.uniform(-0.5, 0.5)
        
        # 4. Pressure follows temperature (Ideal gas law-ish)
        self.pressure = (self.temperature / 300.0) * 100.0 + random.uniform(-0.1, 0.1)
        
        # 5. Safety Checks
        if self.temperature > self.config["thresholds"]["critical_temp"]:
            self.emergency_shutdown("CRITICAL TEMPERATURE OVERLOAD")
        elif self.temperature > self.config["thresholds"]["max_temp"]:
            self.logger.warning(f"High temperature detected: {self.temperature:.2f}K")

    def emergency_shutdown(self, reason="MANUAL SCRAM"):
        if not self.scram_active:
            self.scram_active = True
            self.logger.critical(f"SCRAM ACTIVATED: {reason}")
            print(f"\n[ALERT] {reason}")

    def get_status(self):
        return {
            "temp": f"{self.temperature:.2f}K",
            "press": f"{self.pressure:.2f} bar",
            "flux": f"{self.neutron_flux:.2e}",
            "power": f"{self.power_mw:.2f} MW",
            "rods": f"{self.control_rod_pos}%",
            "coolant": f"{self.coolant_flow}%",
            "scram": "ACTIVE" if self.scram_active else "NOMINAL"
        }
