import json, os
from typing import Optional
from fastapi import FastAPI, Form
from slack import WebClient
from modal import BigIpListModal

app = FastAPI()

client = WebClient(token=os.environ.get('TOKEN'))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/fast")
async def open_fast_prompt(trigger_id: str = Form(...)):
    modal = BigIpListModal()
    bigips = ["52.53.185.182:8443"]
    modal.populate_bigip_list(bigips)

    client.views_open(trigger_id=trigger_id, view=modal.contents)
    return "Opening FAST prompt"

@app.post("/interactive")
async def open_fast_prompt(payload: str = Form(...)):
    json_payload = json.loads(payload)
    print(json_payload)

    if json_payload['type'] == 'block_actions':
        if json_payload['actions'][0]['action_id'] == 'retrieve_templates':
            with open("modal.txt") as modalfile:
                client.views_push(trigger_id=json_payload["trigger_id"], view=json.load(modalfile))
    elif json_payload['type'] == 'view_submission':
        return({"response_action": "clear"})