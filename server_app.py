#
# demo application for http3_server.py
#

import datetime
import os
from urllib.parse import urlencode

import httpbin
from asgiref.wsgi import WsgiToAsgi
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocketDisconnect

ROOT = os.path.dirname(__file__)
LOGS_PATH = os.path.join(ROOT, "htdocs", "logs")
QVIS_URL = "https://qvis.edm.uhasselt.be/"

templates = Jinja2Templates(directory=os.path.join(ROOT, "templates"))
app = Starlette()


@app.websocket_route("/ws")
async def ws(websocket):
    """
    WebSocket echo endpoint.
    """
    if "chat" in websocket.scope["subprotocols"]:
        subprotocol = "chat"
    else:
        subprotocol = None
    await websocket.accept(subprotocol=subprotocol)

    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(message)
    except WebSocketDisconnect:
        pass


app.mount("/httpbin", WsgiToAsgi(httpbin.app))

app.mount("/", StaticFiles(directory=os.path.join(ROOT, "htdocs"), html=True))
