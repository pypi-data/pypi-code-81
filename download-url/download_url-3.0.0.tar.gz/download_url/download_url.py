import traceback
import urllib.request
import os


def download_file(download_url, path_download, file_name):
    """
    A função receberá uma url, referente ao arquivo pdf que se quer fazer o download, o
    caminho (diretorio) onde se quer salvar o arquivo e o nome do arquivo que se deseja
    nomear.

    Entradas
        download_url   : (string)                Url do arquivo alvo
        path_download  : (string)                Caminho (diretório) onde se armazenará o arquivo
        file_name      : (string)                Nome do arquivo 

    Saídas

        (True, filename) : tupla (bool,string)   Retorno sucesso. "Filename = path_download + file_name"
        (-1, traceback)  : tupla (int,string)    Retorno Erro. Falha ao formar o path completo do arquivo
        (-2, traceback)  : tupla (int,string)    Retorno Erro. Falha ao fazer o download do arquivo alvo

    """
    try:
        
        filename = path_download+file_name

    except Exception as e:
        return  (-1,str(traceback.print_exc()))

    try:
        response = urllib.request.urlopen(download_url)    
        file = open(filename , 'wb')
        file.write(response.read())
        file.close()

    except Exception as e:
        return  (-2, str(traceback.print_exc()))

    return (True, filename)

