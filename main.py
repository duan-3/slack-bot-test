from fastapi import FastAPI, requests, Request, Header, APIRouter
from starlette.responses import Response
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_sdk import WebClient
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
client = WebClient(token=os.environ["DUAN_BOT_TOKEN"])

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

@slack_app.view("draw_submit")
def handle_draw_submission(ack, body, client):
    # title = body["view"]["state"]["values"]["title_block"]["title_action"]["value"]
    # winner_num = body["view"]["state"]["values"]["winner_block"]["winner_action"]["value"]
    # timeout = body["view"]["state"]["values"]["time_block"]["time_action"]["value"]
    test = body["view"]
    channel_id = body["channel_id"]
    client.chat_postMessage(
        channel=channel_id,
        # text=f"{title}\n:hooray:당첨자 수 : {winner_num}\n:마감:마감시간 : {timeout}"
        text=f"view -> {test}"
    )
    ack()

#슬래시 커맨드
@slack_app.command("/draw")
def draw_command(ack, body, client):
    ack()
    view = {
            "type": "modal",
            "callback_id": "draw_submit",
            "title": {
                "type": "plain_text",
                "text": "My App",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Super Rapid Draw",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "block_id": "title_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "title-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "무엇을 뽑아 볼까요",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "block_id": "winner_block",
                    "element": {
                        "type": "number_input",
                        "is_decimal_allowed": True,
                        "action_id": "winner-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "당첨자 수",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "block_id": "time_block",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":마감:마감시간"
                    },
                    "accessory": {
                        "type": "timepicker",
                        "initial_time": "13:37",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select time",
                            "emoji": True
                        },
                        "action_id": "time-action"
                    }
                }
            ]
        }
    trigger_id = body["trigger_id"]
    client.views_open(trigger_id=trigger_id, view=view)



#승테스트
@slack_app.message("TEST")
def test_message(event, say):
    channel = event["channel"]
    say("Yeah", channel=channel)

@slack_app.message("무승뽑")
def random_seungjae(client, message):
    channel = message["channel"]
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
    client.chat_postMessage(channel=channel, blocks=blocks)


@slack_app.action("retry")
def get_reseungjae(ack, say):
    ack()
    sjs = [":블루승재:", ":저승재움짤:", ":프링글승재:", ":레드승재:", ":페페승재:", ":아바타승재:", ":타노승재움짤:", ":광대승재:", ":승재:", ":seungjyp:", ":핑크승재:", ":안경승재:", ":짱구승재:"]
    seungjae = random.choice(sjs)
    say(f"{seungjae}")


app.include_router(duan_router, prefix="/duan")

