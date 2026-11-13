import tempfile
import unittest
from pathlib import Path
from ethos_drive.synthetic import get_scenario
from ethos_drive.pipeline import process
from ethos_drive.logger import EventLogger
from ethos_drive.models import Observation

class TestEthosDrive(unittest.TestCase):
    def test_clear_road(self):
        _, d, _ = process(get_scenario("Clear road"))
        self.assertEqual(d.action, "NORMAL (SIMULATED)")
    def test_uncertainty_fallback(self):
        _, d, _ = process(get_scenario("Ambiguous detection"))
        self.assertTrue(d.fallback)
    def test_sensor_failure(self):
        _, d, _ = process([], sensor_ok=False)
        self.assertTrue(d.fallback)
    def test_risk_bounded(self):
        a, _, _ = process([Observation("person", 1.0, 0, 15)])
        self.assertTrue(0 <= a[0].risk <= 1)
    def test_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            logger = EventLogger(Path(tmp) / "events.sqlite3")
            o = get_scenario("Pedestrian crossing")
            a, d, _ = process(o)
            logger.record("synthetic", "Pedestrian crossing", o, a, d)
            self.assertEqual(len(logger.recent()), 1)

if __name__ == "__main__":
    unittest.main()
