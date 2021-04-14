from django.views import View

import fastbot.json
from fastbot import DialogManager, InMemoryDataStore, InMemoryDialogSet
from fastbot.responses import init, end, ContentType, Request
from django.http import JsonResponse

app = DialogManager(data_store=InMemoryDataStore(), dialog_set=InMemoryDialogSet())


@app.root(default="enter_number")
def root_handler(dialog=None, request=None, state=None, **kwargs):
    return init(text="Hello\nPlease enter\n1. Yes \n2. No")


@app.dialogue(name="enter_number")
def selected_choice(dialog=None, request=None, state=None, **kwargs):
    return end(text="You entered request {0}".format(request.text), content_type=ContentType.TEXT)


# django example
class BotRequestHandler(View):

    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        return JsonResponse(app.handle(Request(**body)), encoder=fastbot.json.JSONEncoder)


# console example
rq = Request(channel_type='facebook', session="user-1", text="Hello")
rp = app.handle(rq)
print(rp.json())
rq = Request(channel_type='facebook', session="user-1", text="Hello")
rp = app.handle(rq)
print(rp.json())

# flask
from flask import Flask, Response as FlaskResponse, request, jsonify
import json

api = Flask(__name__)


@api.route("/endpoint", methods=['POST'])
def hello():
    resp = FlaskResponse()
    resp.headers['Content-Type'] = 'application/json'
    return resp


if __name__ == "__main__":
    app.run()

from fastapi import Request, FastAPI

api = FastAPI()


@api.post("/endpoint")
async def get_body(request: Request):
    data = await request.json()
    return app.handle(Request(**data)).json()
