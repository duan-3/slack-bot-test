from fastapi import FastAPI, requests, Request, Header, APIRouter
from starlette.responses import Response
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
import os
import ssl
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
#interaction endpoint
@duan_router.post("/slack/interaction")

# 이벤트 처리
@slack_app.event("app_mention")
def handle_mention(event, say):
    thread_ts = event["ts"]
    say("호", thread_ts=thread_ts)




@slack_app.message("?무승뽑")
def random_seungjae(event, say):
    blocks = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*무승뽑(무한 승재 뽑기)*"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "뽑기",
					"emoji": True
				},
				"value": "click_me_123",
				"action_id": "retry"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": ":블루승재::저승재움짤::프링글승재::레드승재::페페승재::아바타승재::타노승재움짤::광대승재::승재::seungjyp::핑크승재::안경승재::짱구승재:",
				"emoji": True
			}
		}
	]
    say(blocks=blocks)

# @slack_app.action("retry")
# def get_reseungjae(ack, say):
#     ack()
#     sjs = [":블루승재:", ":저승재움짤:", ":프링글승재:", ":레드승재:", ":페페승재:", ":아바타승재:", ":타노승재움짤:", ":광대승재:", ":승재:", ":seungjyp:", ":핑크승재:", ":안경승재:", ":짱구승재:"]
#     seungjae = random.choice(sjs)
#     say(f"{seungjae}")


app.include_router(duan_router, prefix="/duan")

