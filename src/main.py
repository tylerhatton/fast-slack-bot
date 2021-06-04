import json, os, requests
from typing import Optional
from fastapi import FastAPI, Form, HTTPException
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
    elif json_payload['type'] == 'view_submission' and json_payload['view']['callback_id'] == 'template':
        bigip = json_payload['view']['blocks'][1]['text']['text']
        template = json_payload['view']['blocks'][3]['text']['text']
        parameter_values = json_payload['view']['state']['values']
        bigip_username = get_username(creds_file, bigip)
        bigip_password = get_password(creds_file, bigip)

        fast_payload = {
            "name": template,
            "parameters": {}
        }
        # Build parameters for FAST payload
        for parameter in parameter_values:
            parameter_value = parameter_values[parameter][parameter]['value']

            # Trying to identify the correct data type to send to FAST because FAST can't do datatype conversions...
            if "\n" in parameter_value:
                fast_parameter = parameter_value.splitlines()
            elif parameter_value.isnumeric():
                fast_parameter = int(parameter_value)
            else:
                fast_parameter = parameter_value

            fast_payload['parameters'][parameter] = fast_parameter
        # Attempt to send FAST payload
        try:
            response = requests.post(
                'https://' + bigip + '/mgmt/shared/fast/applications',
                auth=(bigip_username, bigip_password),
                json=fast_payload,
                verify=False,
                timeout=10
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise HTTPException(status_code=500, detail="Request Failed")

        # Close all the views and end the modal
        return {
            "response_action": "clear"
        }
