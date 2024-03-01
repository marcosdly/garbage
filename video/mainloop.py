import cv2 as cv
from video.globals import InitConfig
from video.state import Windows
from video.analyze_sprites import find_sprite


def mainloop() -> None:
  cap = cv.VideoCapture(2, cv.CAP_DSHOW)
  cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
  cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
  while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
      continue
    # canny = cv.Canny(frame, 400, 400)
    # cv.imshow(Windows.ORIGINAL, cv.resize(frame, (640, 360)))
    # cv.imshow(Windows.FILTER, cv.resize(canny, (640, 360)))
    path, matches_num = find_sprite(frame)
    if cv.waitKey(1) == ord("q"):
      cv.destroyAllWindows()
      break
  cap.release()
