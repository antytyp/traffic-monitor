import unittest

from src.utils.monitored_region import MonitoredRegion


class TestMonitoredRegion(unittest.TestCase):
    def setUp(self) -> None:
        self.region = MonitoredRegion(name="Test", x=0, y=5, width=10, height=15)

    def test_get_pil_polygon_xy(self) -> None:
        expected_pil_polygon_xy = [(5, 0), (5, 15), (15, 15), (15, 0)]
        self.assertEqual(self.region.get_pil_polygon_xy(), expected_pil_polygon_xy)

    def test_get_np_ranges(self) -> None:
        expected_x_range = slice(0, 15, 1)
        expected_y_range = slice(5, 15, 1)
        expected_z_range = slice(0, 3, 1)

        x_range, y_range, z_range = self.region.get_np_ranges()

        self.assertEqual(x_range, expected_x_range)
        self.assertEqual(y_range, expected_y_range)
        self.assertEqual(z_range, expected_z_range)


if __name__ == "__main__":
    unittest.main()
