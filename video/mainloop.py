import cv2 as cv


def mainloop(shared_stop_bool) -> bool:
  """Processing's main loop

  Args:
      shared_stop_bool (bool): shared boolean signal, check for "stop" signal from user

  Returns:
      bool: status code
  """
  obs_cap = 2
  size = (1920, 1080)
  cap = cv.VideoCapture(obs_cap, cv.CAP_DSHOW)
  cap.set(cv.CAP_PROP_FRAME_WIDTH, size[0])
  cap.set(cv.CAP_PROP_FRAME_HEIGHT, size[1])
  while cap.isOpened():
    with shared_stop_bool.get_lock():
      if shared_stop_bool.value:
        cv.destroyAllWindows()
        return True

    ok, frame = cap.read()
    if not ok:
      continue

    cv.imshow("asdf", frame)
    cv.waitKey(1)
