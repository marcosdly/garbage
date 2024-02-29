import cv2 as cv
from video.net.video import VideoStreams


def mainloop() -> None:
    cap = cv.VideoCapture(2, cv.CAP_DSHOW)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            continue
        _, frame = cv.imencode(".ppm", frame)
        VideoStreams.original.send(bytes(frame))
    cap.release()
