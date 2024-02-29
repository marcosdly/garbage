from multiprocessing import Process
from video.entrypoint import main


class VideoProcess:
    proc: Process | None = None

    @classmethod
    def new_process(cls, **kw) -> None:
        proc = Process(name="video_processing", target=main, kwargs=kw)
        cls.proc = proc
