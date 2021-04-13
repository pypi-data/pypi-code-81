from postx.services import BaseService


class slack(BaseService):
    def _build_message(self, message):
        data = {'blocks': []}
        for k, v in message.get_message().items():
            block = None
            if 'text' in v:
                block = {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": v['text']
                    }
                }
            elif 'link' in v:
                u = v['link'][1]
                t = v['link'][0]
                block = {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<{u}|{t}>"
                    }
                }
            elif 'title' in v:
                block = {
                    "type": "header",
                    "text":
                        {
                            "type": "plain_text",
                            "text": v['title'],
                            "emoji": True
                        }
                }
            elif 'sub' in v:
                t = v['sub']
                block = {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{t}*"
                    }
                }
            elif 'list-ol' in v:
                listIndex = 1
                markdown = ''
                for li in v['list-ol']:
                    markdown += f'{listIndex}. {li}\n'
                    listIndex += 1
                block = {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": markdown
                    }
                }
            elif 'list-ul' in v:
                markdown = ''
                for li in v['list-ul']:
                    markdown += f'\u2022 {li}\n'
                block = {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": markdown
                    }
                }
            if block is not None:
                data['blocks'].append(block)
        return data
