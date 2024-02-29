from server.app import app
from quart import Response


@app.route("/")
async def index():
    with open("client/index.html", "rt") as html:
        return html.read()


@app.route("/index.js")
async def js():
    with open("client/index.js", "rt") as js:
        return Response(response=js.read(), content_type="text/javascript")


@app.route("/state.js")
async def state_js():
    with open("client/state.js", "rt") as js:
        return Response(response=js.read(), content_type="text/javascript")


@app.route("/style.css")
async def css():
    with open("client/style.css", "rt") as css:
        return Response(response=css.read(), content_type="text/css")
