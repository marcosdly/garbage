def main(frame_buffer) -> None:
    from multiprocessing import SimpleQueue
    from typing import cast
    from src.video.transmit import transmit_video

    frame_buffer = cast(SimpleQueue, frame_buffer)
    transmit_video(frame_buffer)
