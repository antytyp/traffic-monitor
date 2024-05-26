from src.utils.monitored_region import MonitoredRegion
from src.utils.utils import get_monitored_regions


def test_get_monitored_regions() -> None:
    region_configs = [
        {"name": "CC1", "x": 450, "y": 1050, "width": 96, "height": 54},
        {"name": "CC2", "x": 500, "y": 1250, "width": 96, "height": 54},
    ]

    expected_monitored_regions = [
        MonitoredRegion(name="CC1", x=450, y=1050, width=96, height=54),
        MonitoredRegion(name="CC2", x=500, y=1250, width=96, height=54),
    ]

    actual_monitored_regions = get_monitored_regions(region_configs)

    assert actual_monitored_regions == expected_monitored_regions
