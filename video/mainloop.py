import cv2 as cv
from video.framework import Darknet


def mainloop() -> bool:
  """Processing's main loop

  Args:
      shared_stop_bool (bool): shared boolean signal, check for "stop" signal from user

  Returns:
      bool: status code
  """
  size = (1920, 1080)
  dnn = Darknet()
  cap = cv.VideoCapture("C:\\Users\\gabas\\Videos\\tibia_swamp_cave.mp4", cv.CAP_FFMPEG)
  cap.set(cv.CAP_PROP_FRAME_WIDTH, size[0])
  cap.set(cv.CAP_PROP_FRAME_HEIGHT, size[1])
  while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
      print("video stream ended (or error?); exiting...")
      break

    dnn.detect(frame)
    dnn.draw_labels(imshow=True)
