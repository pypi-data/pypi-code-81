import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
from xlwt import Workbook, XFStyle
import configparser
import os
import sys
# para salvar o Excel em formato XLSX
# https://stackoverflow.com/questions/9918646/how-to-convert-xls-to-xlsx
import win32com.client as win32
import shutil
import progressbar  #https://gist.github.com/chrissimpkins/2c451bcff7bd7cbcf66e
import tqdm
# as funções auxiliares do MagicFormula
#sys.path.append(sys.path[0].replace("GetQuotes", "mftoolbox"))
#from ..mftoolbox.mftoolbox import *
from mftoolbox import mftoolbox
from constants import header

class cotacoes:

    def __init__(self, STR_LISTA_ATIVOS, STR_DATA_INICIO, STR_DATA_FIM):

        obj_dolar = mftoolbox.UltimaCotacaoDolar()
        STR_HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/39.0.2171.95 Safari/537.36',
                    'Cache-Control': 'no-cache'}

        DTT_DATA_INICIO = datetime.strptime(STR_DATA_INICIO, '%d/%m/%Y')
        DTT_DATA_FIM = datetime.strptime(STR_DATA_FIM, '%d/%m/%Y')
        obj_dolar_historico = mftoolbox.CotacaoDolarHistorico(DTT_DATA_INICIO.strftime('%d/%m/%Y'), date.today().strftime('%d/%m/%Y'))
        STR_URL_COTACOES = 'https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=**********&qtdpregoes=||||||||||'
        STR_URL_DETALHES_ATIVOS = 'http://www.fundamentus.com.br/detalhes.php?papel=**********'
        INT_BIG_CAP = FIL_CONFIG_INI.getint("Ativos", "Big Cap")
        INT_SMALL_CAP = FIL_CONFIG_INI.getint("Ativos", "Small Cap")
        STR_ATIVOS_MANDATORIOS = 'USD', 'IBOV'
        obj_dolar_historico = mftoolbox.CotacaoDolarHistorico(DTT_DATA_INICIO.strftime('%d/%m/%Y'),date.today().strftime('%d/%m/%Y'))
        DTT_NUMERO_PREGOES = datetime.today() - DTT_DATA_INICIO
        lst_acoes = STR_LISTA_ATIVOS.split(',')
        for item in STR_ATIVOS_MANDATORIOS:
            lst_acoes.append(item)  # Sempre inclui IBOV como padrão na lista
        str_linha = 1
        linha_ultimo_registro = 1

        for acao in lst_acoes:
            # -------------------- Início das ações da etapa --------------------
            lista_cells = []
            str_url_temp = STR_URL_COTACOES.replace('**********', acao).replace('||||||||||', str(DTT_NUMERO_PREGOES.days))
            # url = 'https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=' +  acao + '&qtdpregoes=' + str(pregoes.days)
            r = requests.get(str_url_temp, headers=STR_HEADER)
            soup = BeautifulSoup(r.text, 'html.parser')

            # -------------------- Início da carga dos detalhes para cada ação, para achar o tipo de ação: Small, Mid e Big Cap
            str_tipo_capitalizacao = ""
            # if acao != "IBOV" and acao != "USD":
            if acao not in STR_ATIVOS_MANDATORIOS:
                rqt_site = requests.get(STR_URL_DETALHES_ATIVOS.replace('**********', acao), headers=STR_HEADER)
                html_soup = BeautifulSoup(rqt_site.text, 'html.parser')
                prs_data_detalhes_ativos = html_soup.find_all('td')

                flt_valor_mercado_reais = prs_data_detalhes_ativos[21].string  # mudança
                if flt_valor_mercado_reais is None or flt_valor_mercado_reais == '-':  # mudança
                    int_tem_dados_fundamentos = 0
                    flt_valor_mercado_reais = ''
                    flt_valor_mercado_usd = ''
                    str_tipo_capitalizacao = ''
                else:
                    flt_valor_mercado_reais = float(prs_data_detalhes_ativos[21].string.replace(".", "").replace(',', '.'))
                    flt_valor_mercado_usd = flt_valor_mercado_reais / FLT_DOLAR_HOJE
                    if flt_valor_mercado_usd >= INT_BIG_CAP:
                        str_tipo_capitalizacao = 'BIG CAP'
                    elif flt_valor_mercado_usd <= INT_SMALL_CAP:
                        str_tipo_capitalizacao = 'SMALL CAP'
                    else:
                        str_tipo_capitalizacao = 'MID CAP'

            int_registros = 1
            for td in soup.find_all('td'):
                int_registros += 1

            # valor máximo que a progressbar receberá = número de itens na lista que será iterada
            int_valor_maximo_barra = int_registros

            # inicializa a progressbar
            obj_bar = progressbar.ProgressBar(max_value=int_valor_maximo_barra, widgets=lst_widget_def)

            # define largura da barra
            obj_bar.term_width = INT_LARGURA_PROGRESSBAR

            # print('Coleta de dados de ', acao, ' ok!')

            counter = 1
            for td in soup.find_all('td'):
                lista_cells.append(td.text)
                # print(counter, td.text)

                str_novo_texto = str_raiz_mensagem_dinamica + acao.replace("'", "''")
                obj_bar.widgets[int_posicao_dinamico] = obj_bar.widgets[int_posicao_dinamico].replace(STR_DINAMICO_PROGRESSBAR,
                                                                                                      str_novo_texto)
                obj_bar.term_width = INT_LARGURA_PROGRESSBAR + len(str_novo_texto)

                obj_bar.update(counter)
                obj_bar.widgets[int_posicao_dinamico] = obj_bar.widgets[int_posicao_dinamico].replace(str_novo_texto,
                                                                                                      STR_DINAMICO_PROGRESSBAR)
                counter += 1

            int_len = len(lista_cells)
            y = 0
            if acao == "IBOV":
                dtt_ultimo_pregao = datetime.strptime("01/01/1900", '%d/%m/%Y')
                while y + 20 < int_len:
                    date = datetime.strptime(lista_cells[19 + y], '%d/%m/%Y')
                    # obj_dolar2 = mftoolbox.CotacaoDolarData(date.strftime("%d/%m/%Y"))
                    if dtt_ultimo_pregao < date:
                        dtt_ultimo_pregao = date
                    if date >= DTT_DATA_INICIO:
                        sheet1.write(str_linha, 1, acao)
                        sheet1.write(str_linha, 0, date, date_format)
                        sheet1.write(str_linha, 2, float(lista_cells[22 + y].replace(".", "").replace(",", ".")))
                        sheet1.write(str_linha, 3, float(lista_cells[20 + y].replace(".", "").replace(",", ".").replace("%", ""))/100)
                        sheet1.write(str_linha, 4, 0)
                        sheet1.write(str_linha, 5, 0)
                        str_linha = str_linha + 1
                    y = y + 7
            elif acao == "USD":
                for itens in obj_dolar_historico.cotacoes:
                    sheet1.write(str_linha, 1, acao)
                    sheet1.write(str_linha, 0, datetime.strptime(itens[0], "%d/%m/%Y"), date_format)
                    sheet1.write(str_linha, 2, float(itens[1]))
                    str_linha = str_linha + 1
            else:
                while y + 21 < int_len:
                    date = datetime.strptime(lista_cells[21 + y], '%d/%m/%Y')
                    if date >= DTT_DATA_INICIO:
                        sheet1.write(str_linha, 1, acao)
                        sheet1.write(str_linha, 0, datetime.strptime(lista_cells[21+y], "%d/%m/%Y"), date_format)
                        sheet1.write(str_linha, 2, float(lista_cells[24 + y].replace(".", "").replace(",", ".")))
                        sheet1.write(str_linha, 3, float(lista_cells[22 + y].replace(".", "").replace(",", ".").replace("%", ""))/100)
                        sheet1.write(str_linha, 4, lista_cells[28+y])
                        sheet1.write(str_linha, 5, lista_cells[29+y])
                        sheet1.write(str_linha, 6, str_tipo_capitalizacao)
                        str_linha = str_linha + 1
                    y = y + 9
            str_novo_texto = "Sucesso. Ativo " + acao + " carregado. Cotações = " + str(int(str_linha)-linha_ultimo_registro)
            linha_ultimo_registro = str_linha
            obj_bar.term_width = INT_LARGURA_PROGRESSBAR + len(str_novo_texto)
            obj_bar.widgets[int_posicao_dinamico] = obj_bar.widgets[int_posicao_dinamico].replace(STR_DINAMICO_PROGRESSBAR,
                                                                                                  str_novo_texto)
            obj_bar.finish()
            lst_widget_def[int_posicao_dinamico] = STR_DINAMICO_PROGRESSBAR
        print('')
        print('Data do último pregao: {}'.format(dtt_ultimo_pregao.strftime("%d/%m/%Y")))

        # -------------------- Fim das ações da etapa --------------------

    # apresenta a mensagem final de conclusão
    str_novo_texto = "Sucesso. Registros carregados = " + str(str_linha)
    obj_bar.term_width = INT_LARGURA_PROGRESSBAR + len(str_novo_texto)
    obj_bar.widgets[int_posicao_dinamico] = obj_bar.widgets[int_posicao_dinamico].replace(STR_DINAMICO_PROGRESSBAR,
                                                                                          str_novo_texto)
    obj_bar.finish()
    lst_widget_def[int_posicao_dinamico] = STR_DINAMICO_PROGRESSBAR
    # -------------------- Fim da coleta de dados das cotações --------------------

print('')
# print('Finalizando e salvando o XLS em '+STR_DIRETORIO)
dtt_lap_start = datetime.now()
try:
    os.remove(STR_DIRETORIO_SALVAR + STR_NOME_ARQUIVO)
except EFileNotFoundError:
    pass
try:
    os.remove(STR_DIRETORIO_SALVAR + STR_NOME_ARQUIVO + "x")
except FileNotFoundError:
    pass
try:
    wb.save(STR_DIRETORIO_SALVAR + STR_NOME_ARQUIVO)
except Exception as e:
    if os.path.exists(STR_DIRETORIO_SALVAR + STR_NOME_ARQUIVO):
        pass
    else:
        print('Alerta: não foi possível criar o arquivo ' + STR_DIRETORIO_SALVAR + STR_NOME_ARQUIVO)
        pass
excel = win32.DispatchEx("Excel.Application")
wb = excel.Workbooks.Open(STR_DIRETORIO_SALVAR + STR_NOME_ARQUIVO)
try:
    wb.SaveAs(STR_DIRETORIO_SALVAR + STR_NOME_ARQUIVO + "x", FileFormat=51)  # FileFormat = 51 is for .xlsx extension
except Exception as e:
    if os.path.exists(STR_DIRETORIO_SALVAR + STR_NOME_ARQUIVO + "x"):
        pass
    else:
        print('Alerta: não foi possível criar o arquivo ' + STR_DIRETORIO_SALVAR + STR_NOME_ARQUIVO + "x")
        pass
wb.Close()  # FileFormat = 56 is for .xls extension
excel.Application.Quit()

# wb.save(STR_DIRETORIO+STR_NOME_ARQUIVO)

dtt_lap = datetime.now() - dtt_lap_start
print('')
print('|■■■■■■■■■■■■■■■■■■| Elapsed Time: {}, Time: {}, Sucesso. Gravação do arquivo Excel. Cotações = {}'.format(str(dtt_lap).split('.')[0], str(dtt_lap).split('.')[0], len(lst_acoes)))
print('')
print('Tempo de execução (hh:mm:ss.ms) {}'.format(datetime.now() - obj_timestamp.dtt_now))
print('')
if BLN_PAUSA:
    input('Pressione Enter para finalizar...')

def ultimo_pregao(_ativo: 'código do ativo') -> 'texto com a data do último pregão para ' + _ativo + ' no formato DD/MM/AAAA':
    """

    :param _ativo: código do ativo
    :return: texto com a data do último pregão para o ativo no formato DD/MM/AAAA
    """

    url = 'https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=' + ativo + '&qtdpregoes=1'
    r = requests.get(url, headers=mftoolbox.header.header)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.find_all('td')[19].text