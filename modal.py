import requests

class BigIpListModal:
    def __init__(self):
        self.contents = {
            "type": "modal",
            "callback_id": "bigip_list",
            "title": {
                "type": "plain_text",
                "text": "F5 FAST Template",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Next",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "block_id": "bigip_select",
                    "type": "input",
                    "element": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select an F5 BIG-IP",
                            "emoji": True
                        },
                        "options": [],
                        "action_id": "static_select-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Target F5 BIG-IP",
                        "emoji": True
                    }
                }
            ]      
        }

    def populate_bigip_list(self, bigips):
        bigip_list = []
        for bigip in bigips:
            item = {
                "text": {
                    "type": "plain_text",
                    "text": bigip,
                    "emoji": True
                },
                "value": bigip
            }
            bigip_list.append(item)
        
        self.contents['blocks'][0]['element']['options'] = bigip_list
        return

class TemplateListModal:
    def __init__(self):
        self.contents = {
            "type": "modal",
            "callback_id": "template_list",
            "title": {
                "type": "plain_text",
                "text": "F5 FAST Template",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Next",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Back",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Target BIG-IP*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "Placeholder"
                    }
                },
                {
                    "block_id": "template_select",
                    "type": "input",
                    "element": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a FAST Template",
                            "emoji": True
                        },
                        "options": [],
                        "action_id": "static_select-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "FAST Template",
                        "emoji": True
                    }
                }
            ]      
        }

    def populate_template_list(self, bigip, bigip_username, bigip_password):
        response = requests.get(
            'https://' + bigip + '/mgmt/shared/fast/templates/',
            auth=(bigip_username, bigip_password),
            verify=False,
            timeout=10
        )

        template_list = []
        for template in response.json():
            item = {
                "text": {
                    "type": "plain_text",
                    "text": template,
                    "emoji": True
                },
                "value": template
            }
            template_list.append(item)
        
        self.contents['blocks'][1]['text']['text'] = bigip
        self.contents['blocks'][2]['element']['options'] = template_list
        return

class TemplateModal:
    def __init__(self):
        self.contents = {
            "type": "modal",
            "callback_id": "template_list",
            "title": {
                "type": "plain_text",
                "text": "F5 FAST Template",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Back",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Target BIG-IP*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "Placeholder"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*FAST Template*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "Placeholder"
                    }
                }
            ]      
        }

    def populate_template(self, bigip, template, bigip_username, bigip_password):
        self.contents['blocks'][1]['text']['text'] = bigip
        self.contents['blocks'][3]['text']['text'] = template

        response = requests.get(
            'https://' + bigip + '/mgmt/shared/fast/templates/' + template,
            auth=(bigip_username, bigip_password),
            verify=False,
            timeout=10
        )

        template_properties = response.json()['_parametersSchema']['properties']

        for template in template_properties.keys():
            template_type = template_properties[template]['type']
            template_default = str(template_properties[template].get('default')) or ' '

            if template_type == 'string' or template_type == 'integer':
                self.contents['blocks'].append(
                    {
                        "type": "input",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": template,
                            "placeholder": {
                                "type": "plain_text",
                                "text": str(template_default)
                            }
                        },
                        "label": {
                            "type": "plain_text",
                            "text": template
                        }
                    } 
                )
        return