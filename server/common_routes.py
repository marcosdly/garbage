from server.app import app
from quart import Response
import os
from pathlib import Path

with os.scandir("dist/client") as scan:
  DIST_CLIENT = {entry.name: entry for entry in scan}


@app.route("/")
async def index():
  with open("dist/client/index.html", "rt") as html:
    return Response(html.read(), 200, content_type="text/html")


@app.route("/<string:asset>")
async def assets(asset: str):
  if asset not in DIST_CLIENT:
    return Response(status=404)

  path = Path(DIST_CLIENT[asset].path)
  with open(str(path), "rt") as file:
    content = "text/plain"
    match path.suffix:
      case ".js":
        content = "text/javascript"
      case ".css":
        content = "text/css"
      case ".json":
        content = "application/json"
      case ".html":
        content = "text/html"

    return Response(file.read(), 200, content_type=content)
