import unittest
import os
import json
from src.reactor_core import ReactorCore

class TestEnhancedReactor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temp config for testing
        cls.test_config = "test_config.json"
        config = {
            "reactor_name": "TEST-UNIT-01",
            "initial_state": {"temperature": 300, "pressure": 100, "neutron_flux": 1e8, "control_rod_pos": 50},
            "thresholds": {"max_temp": 500, "critical_temp": 600, "max_pressure": 150},
            "coefficients": {"heating_rate": 0.1, "cooling_rate": 0.1, "flux_multiplier": 1.0}
        }
        with open(cls.test_config, "w") as f:
            json.dump(config, f)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_config):
            os.remove(cls.test_config)

    def setUp(self):
        self.reactor = ReactorCore(config_path=self.test_config)

    def test_rod_adjustment(self):
        self.reactor.update_control_rods(80)
        self.assertEqual(self.reactor.control_rod_pos, 80)
        
        self.reactor.update_control_rods(150) # Should cap at 100
        self.assertEqual(self.reactor.control_rod_pos, 100)

    def test_physics_step_flux(self):
        initial_flux = self.reactor.neutron_flux
        self.reactor.update_control_rods(100) # Full exposure
        self.reactor.step()
        self.assertGreater(self.reactor.neutron_flux, initial_flux)

    def test_scram_mechanics(self):
        self.reactor.emergency_shutdown("TEST SCRAM")
        self.assertTrue(self.reactor.scram_active)
        self.reactor.step()
        self.assertEqual(self.reactor.control_rod_pos, 0)
        self.assertEqual(self.reactor.coolant_flow, 100)

    def test_logging_creation(self):
        self.reactor.update_control_rods(10)
        self.assertTrue(os.path.exists("logs/reactor.log"))

if __name__ == '__main__':
    unittest.main()
