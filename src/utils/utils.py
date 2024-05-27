from typing import List

from src.utils.monitored_region import MonitoredRegion


def get_monitored_regions(region_configs: List[dict]) -> List[MonitoredRegion]:
    monitored_regions = []

    for region_config in region_configs:
        monitored_regions.append(MonitoredRegion(**region_config))

    return monitored_regions
