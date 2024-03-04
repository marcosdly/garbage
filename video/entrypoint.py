def main(return_bool: bool, stop_bool: bool):
  from video.mainloop import mainloop

  with stop_bool.get_lock():
    if stop_bool.value:
      stop_bool.value = False

  ok = mainloop(stop_bool)

  with return_bool.get_lock():
    # Forcing nested code to not touch memory shared return value
    if ok:
      return_bool.value = True
    return_bool.value = False
