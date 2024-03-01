from server.app import app, VideoQueue
from quart import Response, request
from queue import Empty, Full


@app.route("/video/original", methods=["GET", "POST"])  # type: ignore
async def post_original() -> int | Response:
  if request.method not in ["GET", "POST"]:
    return Response(status=404)

  if request.method == "POST":
    try:
      VideoQueue.original.put_nowait(await request.get_data(cache=False))
    except Full:
      pass
    return Response(status=200)

  frame: bytes | None = None
  try:
    frame = VideoQueue.original.get_nowait()
  except Empty:
    pass

  if frame is None:
    frame = bytes()

  return Response(response=frame, status=200, content_type="video/mp4")
