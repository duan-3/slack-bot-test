from fastapi import FastAPI, requests, Request, Header, APIRouter
from starlette.responses import Response
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
import os
import ssl
import random
ssl._create_default_https_context = ssl._create_unverified_context

app = FastAPI()
duan_router = APIRouter()

slack_app = App(
    token=os.environ["DUAN_BOT_TOKEN"],
    signing_secret=os.environ["DUAN_BOT_SIGNING_SECRET"]
)


@app.get("/")
async def root():
    return Response


# 슬랙 이벤트 수신
@duan_router.post("/slack/events")
async def slack_events(request: Request):
    handler = SlackRequestHandler(slack_app)
    return await handler.handle(request)

# 이벤트 처리
@slack_app.event("app_mention")
def handle_mention(event, say):
    thread_ts = event["ts"]
    say("호", thread_ts=thread_ts)
