from quart import Quart
from queue import Queue
from typing import NamedTuple


class VideoQueueType(NamedTuple):
  original: Queue = Queue(1)


VideoQueue = VideoQueueType()


app = Quart(__name__)
