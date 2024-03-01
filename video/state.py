from typing import NamedTuple


class WindowsType(NamedTuple):
  SPRITE: str = "SPRITE"
  ORIGINAL: str = "ORIGINAL"
  FILTER: str = "FILTER"
  KEYPOINTS: str = "KEYPOINTS"


Windows = WindowsType()
