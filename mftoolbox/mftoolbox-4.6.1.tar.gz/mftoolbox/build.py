import configparser as _configparser
from _datetime import datetime as _datetime
import os as _os
import sys
#sys.path.append('C:\\Users\\coliveira\\OneDrive\\Coding\\Python\\MFToolbox\\')
from mftoolbox import encoding

class Build:
    """
    O controle de build é feito através da data e hora em que o arquivo do Magic Formula foi salvo pela última vez.
    Se a data do arquivo for mais recente do que está registrado no controle de build, o número do build
        será incrementado em 1.
    Se o arquivo de build ainda não existir, será criado com o nome da versão atual (hardcoded), build=0, data de
        atualização = data que o arquivo do Magic Formula foi salvo pela última vez.
    Se o arquivo de build existir e já houver uma entrada para o nome da versão atual, compara o horário da última
        gravação do Magic Formula. Se a última gravação for mais recente do que o registro no controle de build,
        este será incrementado em 1.
    Se o arquivo de build existir e não houver uma entrada para o nome da versão atual, esta será criada com
        o nome da versão atual (hardcoded), build=0, data de atualização = data que o arquivo do Magic Formula
        foi salvo pela última vez.
    07/10/19: controle para definir build diferente por data apenas ou por data e hora. 0 para data e 1 para data e hora
    """
    def __init__(self, VersaoAtual, FileName, Controle):

        self.str_versao_atual = VersaoAtual
        self.str_nome_arquivo_build = 'BuildHistory.txt'
        self.str_encoding = encoding.encoding()
        self.str_nome_arquivo_chamada = FileName

        # data em que o arquivo atual foi salvo
        self.dtt_ultima_atualizacao = _os.stat(_os.path.basename(FileName)).st_mtime

        # cria se não existe o arquivo com os dados do build atual, senão, abre o arquivo existente
        if not _os.path.isfile(self.str_nome_arquivo_build):
            dic_build_content = _configparser.ConfigParser()
            dic_build_content[self.str_versao_atual] = {'build': '0',
                                                   'atualização': str(self.dtt_ultima_atualizacao),
                                                   'data': _datetime.fromtimestamp(
                                                       self.dtt_ultima_atualizacao).strftime('%d-%m-%Y %H:%M:%S')}

            with open(self.str_nome_arquivo_build, 'w', encoding=self.str_encoding) as fil_build:
                dic_build_content.write(fil_build)
                fil_build.close()
        else:
            dic_build_content = _configparser.ConfigParser()
            dic_build_content.read(self.str_nome_arquivo_build, encoding=self.str_encoding)

        # se não houver entrada para a versão atual, cria (anexando ao arquivo existente)
        # Se houver, verifica se os dados do build são iguais
        try:
            self.int_numero_build = dic_build_content.getint(self.str_versao_atual, 'build')
            flt_atualizacao = dic_build_content.getfloat(self.str_versao_atual, "atualização")
            self.str_data_build = _datetime.fromtimestamp(self.dtt_ultima_atualizacao).strftime('%d-%m-%Y %H:%M:%S')

            # se a data da última revisão do arquivo for diferente da informação do arquivo de build, aumenta o número do build
            # e atualiza o arquivo de controle de build
            if (self.dtt_ultima_atualizacao != flt_atualizacao and Controle == 1) or (_datetime.fromtimestamp(self.dtt_ultima_atualizacao).strftime('%d-%m-%Y') != _datetime.fromtimestamp(flt_atualizacao).strftime('%d-%m-%Y') and Controle == 0):
                self.int_numero_build = self.int_numero_build + 1
                dic_build_content.set(self.str_versao_atual, 'build', str(self.int_numero_build))
                dic_build_content.set(self.str_versao_atual, 'atualização', str(self.dtt_ultima_atualizacao))
                dic_build_content.set(self.str_versao_atual, 'data',
                                      _datetime.fromtimestamp(self.dtt_ultima_atualizacao).strftime(
                                          '%d-%m-%Y %H:%M:%S'))
                # sobrescreve o arquivo
                with open(self.str_nome_arquivo_build, 'w+', encoding=self.str_encoding) as fil_build:
                    dic_build_content.write(fil_build)
                fil_build.close()
        except:
            self.int_numero_build = 0
            dic_build_content = _configparser.ConfigParser()
            dic_build_content[self.str_versao_atual] = {'build': self.int_numero_build,
                                                   'atualização': str(self.dtt_ultima_atualizacao),
                                                   'data': _datetime.fromtimestamp(
                                                       self.dtt_ultima_atualizacao).strftime('%d-%m-%Y %H:%M:%S')}
            # adiciona ao que já está no arquivo
            with open(self.str_nome_arquivo_build, 'a', encoding=self.str_encoding) as fil_build:
                dic_build_content.write(fil_build)
            fil_build.close()

        self.str_ultima_atualizacao = _datetime.fromtimestamp(self.dtt_ultima_atualizacao).strftime(
            '%d-%m-%Y %H:%M:%S')
        self.txt_int_numero_build = str(self.int_numero_build)