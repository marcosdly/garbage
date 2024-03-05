import os
import time
import cv2 as cv
from PIL import Image


def main():
  obs_cap = 2
  video = cv.VideoCapture(obs_cap, cv.CAP_DSHOW)
  w, h = (1920, 1080)
  video.set(cv.CAP_PROP_FRAME_WIDTH, w)
  video.set(cv.CAP_PROP_FRAME_HEIGHT, h)

  path = "dataset"
  images = 450
  i = 0
  if not os.path.isdir(path):
    os.makedirs(path, exist_ok=True)
  while True:
    if not video.isOpened():
      print("Video capture device not available")
      break
    if i >= images:
      print("All images collected successfully")
      break
    ok, frame = video.read()
    if not ok:
      continue
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    Image.fromarray(frame).save(f"{path}/{i}_img.jpg")
    i += 1
    time.sleep(1)


if __name__ == "__main__":
  main()
