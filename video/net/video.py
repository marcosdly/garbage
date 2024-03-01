from typing import NamedTuple
from video.globals import InitConfig
import requests


class Stream:
  def __init__(self, url_segment: str) -> None:
    self.url_segment = url_segment
    self.url = InitConfig["url"] + f"/video/{self.url_segment}"

  def send(self, frame: bytes) -> None:
    requests.post(self.url, frame)


class VideoStreamsType(NamedTuple):
  original: Stream = Stream("original")


VideoStreams = VideoStreamsType()
