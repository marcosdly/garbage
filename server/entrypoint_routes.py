from server.app import app
from quart import request, Response
from server.process import VideoProcess
from urllib.parse import urlparse


@app.route("/app/state", methods=["POST"])
async def state():
  data = await request.json

  if data["type"] == "entrypoint":
    if data["state"] == "stop":
      if VideoProcess.proc is None:
        return Response(status=200)
      if not VideoProcess.proc.is_alive():
        VideoProcess.proc.close()
        return Response(status=200)
      VideoProcess.proc.terminate()
      VideoProcess.proc.close()
      return Response(status=200)

    if data["state"] == "start":
      url = urlparse(request.base_url)
      VideoProcess.new_process(
        host=url.hostname, port=url.port, url=f"{url.scheme}://{url.netloc}"
      )
      VideoProcess.proc.start()
      return Response(status=200)

  return Response(status=200)
