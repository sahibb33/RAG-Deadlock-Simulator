"""Basic automated tests. Run: python -m unittest -v"""
import unittest
import simulation
from deadlock_detection import detect_deadlock, resolve_deadlock


class DeadlockSimulatorTests(unittest.TestCase):
    def setUp(self):
        simulation.reset_simulation()

    def make_two_process_deadlock(self):
        simulation.add_process("P1")
        simulation.add_process("P2")
        simulation.add_resource("R1")
        simulation.add_resource("R2")
        simulation.allocate_resource("P1", "R1")
        simulation.allocate_resource("P2", "R2")
        simulation.request_resource("P1", "R2")
        simulation.request_resource("P2", "R1")

    def test_detects_two_process_deadlock(self):
        self.make_two_process_deadlock()
        result = detect_deadlock(simulation.get_system_state())
        self.assertTrue(result["deadlock"])
        self.assertEqual(result["processes"], ["P1", "P2"])
        self.assertEqual(result["resources"], ["R1", "R2"])

    def test_no_deadlock_when_no_cycle(self):
        simulation.add_process("P1")
        simulation.add_resource("R1")
        simulation.allocate_resource("P1", "R1")
        result = detect_deadlock(simulation.get_system_state())
        self.assertFalse(result["deadlock"])

    def test_recovery_terminates_selected_process(self):
        self.make_two_process_deadlock()
        result = resolve_deadlock(simulation.get_system_state(), "P2")
        self.assertTrue(result["success"])
        self.assertNotIn("P2", result["system_state"]["processes"])
        self.assertFalse(result["deadlock_status"]["deadlock"])

    def test_cannot_allocate_already_owned_resource(self):
        simulation.add_process("P1")
        simulation.add_process("P2")
        simulation.add_resource("R1")
        simulation.allocate_resource("P1", "R1")
        result = simulation.allocate_resource("P2", "R1")
        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
