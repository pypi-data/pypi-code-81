#encoding:utf-8
# import urllib
# import urllib2
import json
import textwrap
import time
import requests
import cfscrape
import re

class SMSMasivo(dict):
    ''' Objeto para enviar sms. '''

    def __init__(self, apikey, pruebas=False):
        self.apikey = apikey
        self.pruebas = pruebas

    def split_messages(self, message):
        """separa un mensaje largo en varios indicando el numero de mensaje en el mensaje. """
        mensajes_split = textwrap.wrap(message, 156)
        total = len(mensajes_split)
        messages = []
        for index, message in enumerate(mensajes_split):
            count = index + 1
            message += ' {0}/{1}'.format(count, total)
            messages.append(message)
        return messages

    def send_unique(self, mensaje, telefono, numregion, voz):
        # parametros_dic = {'apikey': self.apikey, 'mensaje': mensaje, 'numcelular': telefono, 'numregion': numregion}
        sandbox=0
        # if self.pruebas:
        #     sandbox = 1
        # else:
        #     sandbox=0
        # # sandbox = 1
        print("-----",self.pruebas)
        print(sandbox)
        telefono = telefono.encode('utf-8')
        telefono = re.sub("[^0-9]", "", str(telefono))
        print(telefono)

        # parametros = urllib.urlencode(parametros_dic)
        # headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
        #        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        #        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        #        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        #        'Accept-Encoding': 'none',
        #        'Accept-Language': 'en-US,en;q=0.8',
        #        'Connection': 'keep-alive'}
        # request_sms = urllib2.Request('https://app.smsmasivos.com.mx/components/api/api.envio.sms.php', parametros, headers)
        # opener = urllib2.build_opener()
        # respuesta = opener.open(request_sms).read()
        # print mensaje
        targetURL = "https://api.smsmasivos.com.mx/sms/send"
        headers = {
          "Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'apikey':self.apikey,
        }
        data = {
          'message':mensaje,
          'numbers':telefono,
          'country_code':numregion,
          'sandbox':sandbox,
        }
        scraper = cfscrape.create_scraper()
        r = scraper.post(url = targetURL, data = data, headers = headers)

        print("*********************************")
        print(r.text)
        print("*********************************")
        return json.loads(r.text)

    def send(self, mensaje, telefono, numregion=52, voz=False):
        """
        enviar mensaje multiple si se pasa de 160 caracteres
        """
        if len(mensaje) > 160:
            messages = self.split_messages(mensaje)
            for message in messages:
                self.send_unique(message, telefono, numregion, voz)
                time.sleep(1)
        else:
            return self.send_unique(mensaje, telefono, numregion, voz)

    def multisend(self, mensaje, telefono, numregion=52):
        # parametros_dic = {'apikey': self.apikey, 'mensaje': mensaje, 'numcelular': telefono, 'numregion': numregion}

        sandbox=0
        # if self.pruebas:
        #     sandbox = 1
        # else:
        #     sandbox=0
        # # sandbox = 1
        print("-----",self.pruebas)
        print(sandbox)
        telefono = telefono.encode('utf-8')
        telefono = re.sub("[^0-9]", "", str(telefono))
        print(telefono)
        # parametros = urllib.urlencode(parametros_dic)
        # headers = {
        #         "Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
        #        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        #        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        #        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        #        'Accept-Encoding': 'none',
        #        'Accept-Language': 'en-US,en;q=0.8',
        #        'Connection': 'keep-alive'}
        # request_sms = urllib2.Request('https://app.smsmasivos.com.mx/components/api/api.multienvio.sms.php', parametros, headers)
        # opener = urllib2.build_opener()
        # respuesta = opener.open(request_sms).read()
        
        targetURL = "https://api.smsmasivos.com.mx/sms/send"
        headers = {
          "Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'apikey':self.apikey,
        }
        data = {
          'message':mensaje,
          'numbers':telefono,
          'country_code':numregion,
          'sandbox':sandbox,
        }
        scraper = cfscrape.create_scraper()
        r = scraper.post(url = targetURL, data = data, headers = headers)

        print("*********************************")
        print(r.text)
        print("*********************************")
        return json.loads(r.text)

    def credito(self):
        # parametros = urllib.urlencode({'apikey': self.apikey})
        # headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
        #         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        #        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        #        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        #        'Accept-Encoding': 'none',
        #        'Accept-Language': 'en-US,en;q=0.8',
        #        'Connection': 'keep-alive'}
        # # request_sms = urllib2.Request('http://www.smsmasivos.com.mx/sms/api.credito.new.php', parametros, headers)
        # request_sms = urllib2.Request('https://app.smsmasivos.com.mx/components/api/api.credito.php', parametros, headers)
        # opener = urllib2.build_opener()
        # respuesta = opener.open(request_sms).read()
        targetURL = "https://api.smsmasivos.com.mx/credits/consult"
        headers = {
          "Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'apikey':self.apikey,
        }

        scraper = cfscrape.create_scraper()
        r = scraper.post(url = targetURL, data = {}, headers = headers)

        print("*********************************")
        print(r.text)
        print("*********************************")
        return json.loads(r.text)