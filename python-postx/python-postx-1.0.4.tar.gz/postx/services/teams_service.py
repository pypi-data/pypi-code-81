from postx.services import BaseService


class teams(BaseService):
    def _build_message(self, message):
        data = {
            "type":
                "message",
            "attachments":
                [
                    {
                        "contentType":
                            "application/vnd.microsoft.card.adaptive",
                        "contentUrl":
                            None,
                        "content":
                            {
                                "$schema":
                                    "http://adaptivecards.io/schemas/adaptive-card.json",
                                "type":
                                    "AdaptiveCard",
                                "version":
                                    "1.2",
                                "body": []
                            }
                    }
                ]
        }
        for k, v in message.get_message().items():
            block = None
            if 'text' in v:
                block = {"type": "TextBlock", "text": v['text']}
            elif 'link' in v:
                u = v['link'][1]
                t = v['link'][0]
                block = {"type": "TextBlock", "text": f"[{t}]({u})"}
            elif 'title' in v:
                block = {
                    "type": "TextBlock",
                    "text": v['title'],
                    "weight": "bolder",
                    "size": "large"
                }
            elif 'sub' in v:
                block = {
                    "type": "TextBlock",
                    "text": v['sub'],
                    "weight": "bolder",
                    "size": "medium",
                    "wrap": True
                }
            elif 'list-ol' in v:
                listIndex = 1
                markdown = ''
                for li in v['list-ol']:
                    markdown += f'{listIndex}. {li}\r'
                    listIndex += 1
                block = {"type": "TextBlock", "text": markdown}
            elif 'list-ul' in v:
                markdown = ''
                for li in v['list-ul']:
                    markdown += f'- {li}\r'
                block = {"type": "TextBlock", "text": markdown}
            if block is not None:
                data['attachments'][0]['content']['body'].append(block)
        return data
