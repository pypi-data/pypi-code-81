import json
import logging
import traceback
from datetime import datetime
import requests
from pytz import timezone


class LoggingELK:

    def __init__(self, insert_elk, elk_host):
        """
        :param insert_elk: true para inserir os dados automaticamente no indice do ELK
        :param elk_host: ip publico do ELK
        """
        self.elk_host = elk_host  # elk host ip address
        self.index_elk_info = "info-logs"  # elk info logs index name
        self.index_elk_warning = "warning-logs"  # elk warning logs index name
        self.index_elk_errors = "errors-logs"  # elk errors logs index name
        self.translate_index_name = {"error": self.index_elk_errors, "warning": self.index_elk_warning, "info": self.index_elk_info}
        self.insert_elk = insert_elk  # if true, will auto insert the logging to the correct index when printing
        self.format = '%(asctime)s %(levelname)s {%(module)s} [%(funcName)s] %(message)s'  # Use the specified format string for the handler.
        self.infos_about_execution = self.parse_full_stack(traceback.extract_stack())
        self.time_zone = 'America/Sao_Paulo'
        logging.basicConfig(format=self.format, datefmt='%Y-%m-%d,%H:%M:%S:%f', level=logging.INFO)

        # precisamos criar o indice avisando qual o tipo do campo pro elk ficar no jeito
        headers = {
            'Content-Type': "application/json",
        }

        date_payload = {
            "mappings": {
                "properties": {
                    "date": {
                        "type": "date"
                    }
                }
            }
        }
        for key in self.translate_index_name:
            parsed_url = "{}{}/_doc/".format(self.elk_host, self.translate_index_name[key])
            try:
                requests.request("POST", parsed_url, data=json.dumps(date_payload), headers=headers)
            except:
                print("Não foi possível criar o indice, atenção!")
    @staticmethod
    def parse_full_stack(full_traceback):
        item = full_traceback[len(full_traceback) - 2]
        return {"filename": item.filename, "line": item.line, "lineno": item.lineno, "locals": item.locals, "name": item.name}

    def check_params(self):
        if self.elk_host == "" and self.insert_elk is True:
            # não da pra inserir sem falar qual o host
            raise ValueError("É necessário definir qual o HOST do ELK caso auto_insert = True")

    def info(self, data: str):
        """
            Exibe e/ou insere algum log do tipo Info

            :param data: data that we will display or saved
            :return: None
        """

        self.check_params()
        self.insert_payload(data, "info")

        logging.info(data)

    def warning(self, data: str):
        """
            Exibe e/ou insere algum log do tipo Warning

            :param data: data that we will display or saved
            :return: None
        """
        self.check_params()
        self.insert_payload(data, "warning")
        logging.warning(data)

    def error(self, data: str):
        """
            Exibe e/ou insere algum log do tipo Error

            :param data: data that we will display or saved
            :return:
        """

        self.check_params()
        self.insert_payload(data, "error")

        logging.error(data)

    def insert_payload(self, data: str, log_type: str):

        if self.insert_elk is True:

            headers = {
                'Content-Type': "application/json",
            }

            # precisamos fazer isso pra garantir que todos os serviços enviarão com o mesmo fuso
            data_e_hora_atuais = datetime.now()
            fuso_horario = timezone(self.time_zone)
            data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario).isoformat(timespec='seconds')

            # o data é sempre uma string que representa o que o usuario quis "logar", vamos converter e obter mais informacoes
            payload = {}
            for key in self.infos_about_execution.keys():
                payload[key] = self.infos_about_execution[key]
            payload['log_type'] = log_type

            if type(data) == str:
                payload['value'] = data
            else:
                payload = data

            payload['date'] = data_e_hora_sao_paulo

            parsed_url = "{}{}/_doc/".format(self.elk_host, self.translate_index_name[log_type])
            try:
                response = requests.request("POST", parsed_url, data=json.dumps(payload), headers=headers)
                if response.status_code == 201 or response.status_code == 200:
                    pass
                else:
                    logging.warning("Não foi possível inserir o LOG do tipo {} no indice {}, status_code gerado: {}".format(log_type, self.translate_index_name[log_type], response.status_code))

            except Exception as error:
                logging.warning("Não foi possível inserir o LOG do tipo {} no indice {}, status_code gerado: {}".format(log_type, self.translate_index_name[log_type], error))
