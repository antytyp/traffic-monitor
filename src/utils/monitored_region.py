from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class MonitoredRegion:
    name: str
    x: int
    y: int
    width: int
    height: int

    def get_pil_polygon_xy(self) -> List[tuple]:
        p1 = (self.y, self.x)
        p2 = (self.y, self.x + self.height)
        p3 = (self.y + self.width, self.x + self.height)
        p4 = (self.y + self.width, self.x)

        return [p1, p2, p3, p4]

    def get_np_ranges(self) -> tuple:
        x_range = slice(self.x, self.x + self.height, 1)
        y_range = slice(self.y, self.y + self.width, 1)
        z_range = slice(0, 3, 1)

        return x_range, y_range, z_range
