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
                    "block_id": "bigip_select",
                    "type": "input",
                    "element": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "FAST Template",
                            "emoji": True
                        },
                        "options": [],
                        "action_id": "static_select-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Select a FAST Template",
                        "emoji": True
                    }
                }
            ]      
        }

    def populate_template_list(self, bigips):
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