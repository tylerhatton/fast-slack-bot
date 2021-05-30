import json, os
from typing import Optional
from fastapi import FastAPI, Form
from slack import WebClient
from modal import BigIpListModal, TemplateListModal, TemplateModal
from credentials import get_hosts, get_username, get_password

app = FastAPI()

client = WebClient(token=os.environ.get('TOKEN'))

creds_file = 'credentials.json'

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/fast")
async def open_fast_prompt(trigger_id: str = Form(...)):
    modal = BigIpListModal()
    bigips = get_hosts(creds_file)
    modal.populate_bigip_list(bigips)

    client.views_open(trigger_id=trigger_id, view=modal.contents)
    return "Opening FAST prompt"

@app.post("/interactive")
async def open_fast_prompt(payload: str = Form(...)):
    json_payload = json.loads(payload)
    print(json_payload)

    if json_payload['type'] == 'view_submission' and json_payload['view']['callback_id'] == 'bigip_list':
        modal = TemplateListModal()
        bigip = json_payload['view']['state']['values']['bigip_select']['static_select-action']['selected_option']['value']
        bigip_username = get_username(creds_file, bigip)
        bigip_password = get_password(creds_file, bigip)

        modal.populate_template_list(bigip, bigip_username, bigip_password)

        return({
            "response_action": "push",
            "view": modal.contents
        })
    elif json_payload['type'] == 'view_submission' and json_payload['view']['callback_id'] == 'template_list':
        modal = TemplateModal()
        bigip = json_payload['view']['blocks'][1]['text']['text']
        template = json_payload['view']['state']['values']['template_select']['static_select-action']['selected_option']['value']
        bigip_username = get_username(creds_file, bigip)
        bigip_password = get_password(creds_file, bigip)

        modal.populate_template(bigip, template, bigip_username, bigip_password)

        return({
            "response_action": "push",
            "view": modal.contents
        })
