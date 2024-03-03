from server.app import app
from quart import Response, request
from os import path
from base64 import b64encode, b64decode

valid_types = ["player", "enemy"]
valid_states = ["front", "back", "dead"]
base64_headers = {"Content-Transfer-Encoding": "base64"}


@app.route("/app/character/<string:type>/<string:state>", methods=["GET", "POST"])
async def character_state(type: str, state: str):
  if type not in valid_types:
    return Response("incorrect character type", status=406)

  if state not in valid_states:
    return Response("incorrect character state", status=406)

  filename = f"state/character/{type}/{state}.png"

  if request.method == "GET":
    if not path.isfile(filename):
      return Response("there is not an image saved anywhere", status=404)

    encoded = bytes()
    with open(filename, "rb") as file:
      encoded = b64encode(file.read())

    return Response(encoded, status=200, headers=base64_headers)

  encoded = await request.get_data(cache=False)
  decoded = b64decode(encoded)
  with open(filename, "wb") as file:
    file.write(decoded)

  return Response(status=200)
