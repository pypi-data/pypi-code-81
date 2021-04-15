import json

from cc_py_commons.sns.sns_service import SnsService

class ParsedCarrierNotification:

  def __init__(self, app_config):
    self._app_config = app_config

  def send(self, parsed_carrier, c4_account_id, import_stats_id):
    message = '{' + f'"accountId" : {c4_account_id}, ' \
                    f'"parsedCarrier" : {json.dumps(parsed_carrier)}, ' \
                    f'"importStatsId": "{import_stats_id}", ' \
                    f'"subject" : "{self._app_config.PARSED_CARRIER_SNS_SUBJECT}", ' \
                    f'"className":  "{self._app_config.PARSED_CARRIER_SNS_CLASS_NAME}"' + '}'
    sns_service = SnsService()
    sns_service.send(self._app_config.PARSED_CARRIER_SNS_TOPIC_ARN,
      self._app_config.PARSED_CARRIER_SNS_SUBJECT, message)
