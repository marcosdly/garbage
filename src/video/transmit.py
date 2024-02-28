import cv2 as cv
from multiprocessing import SimpleQueue
from PIL.Image import fromarray, Resampling  # type: ignore


def transmit_video(frame_buffer: SimpleQueue) -> None:
    video = cv.VideoCapture(2, cv.CAP_DSHOW)
    while video.isOpened():
        ok, frame = video.read()
        if not ok:
            break
        photo = fromarray(frame).resize((1052, 592), Resampling.LANCZOS)
        frame_buffer.put(photo)
