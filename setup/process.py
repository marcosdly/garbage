from multiprocessing import Process, Value
from video.entrypoint import main
from ctypes import c_bool


class _ManagerType:
  def __init__(self):
    self.success = Value(c_bool, False, lock=True)
    self._stop_bool = Value(c_bool, False, lock=True)

    self.proc = Process(
      target=main, name="entrypoint", args=(self.success, self._stop_bool)
    )

  def stop(self):
    with self._stop_bool.get_lock():
      # Process is loop based so it can easily check for it each time
      # If process start with it as True, it will be set back to False
      self._stop_bool.value = True


Manager = _ManagerType()
