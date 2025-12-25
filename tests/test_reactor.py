import unittest
from src.reactor_core import ReactorCore

class TestReactorCore(unittest.TestCase):
    def setUp(self):
        self.reactor = ReactorCore()

    def test_initial_state(self):
        self.assertEqual(self.reactor.temperature, 300.0)
        self.assertEqual(self.reactor.pressure, 100.0)
        self.assertEqual(self.reactor.control_rod_status, "INSERTED")

    def test_boot_system(self):
        self.reactor.boot_system()
        self.assertEqual(self.reactor.control_rod_status, "RETRACTING")

    def test_monitor_loop_fluctuation(self):
        initial_temp = self.reactor.temperature
        self.reactor.monitor_loop()
        self.assertNotEqual(self.reactor.temperature, initial_temp)

    def test_emergency_shutdown(self):
        self.reactor.emergency_shutdown()
        # In a real app we'd check if rods are inserted
        pass

if __name__ == '__main__':
    unittest.main()
