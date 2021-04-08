import yagmail
from loguru import logger


def send_email(title, message, to):
    if title is None or message is None or to is None:
        logger.info('param required,title:{},message:{},to:{}'.format(title, message, to))
    yag_server = yagmail.SMTP(user='riskerat2688@qq.com', password='xogporujfqgabifh', host='smtp.qq.com')
    yag_server.send(to, title, message)
    yag_server.close()
