import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
#sys.path.append('C:\\Users\\coliveira\\OneDrive\\Coding\\Python\\MFToolbox\\')
from mftoolbox import constants, funcs
import time
from mftoolbox.init_selenium import Browser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

def ultimo_preco(crypto='', **kwargs):
    """
    Busca no site Tradingview.com o nome de pregão de um crypto, a última cotação, seu horário,
    ganho monetário e percentual

    :param crypto: código da crypto
    :param __delay = x, x em seundos
    :return: tuple [ticker, nome de pregão, cotacao, horario, variação monetária, variação percentual
    """

    if crypto == '':
        return (['Crypto não informado', '','', ''])

    try:
        __browser = kwargs['browser']
        if __browser.__class__.__name__ != 'Browser':
            raise NameError('Objeto passado não é da classe Browser')
        __fecha_browser = False
    except:
        __browser = Browser(clean=True, hide=True)
        __fecha_browser = True

    __wait = WebDriverWait(__browser,10)

    __url = 'https://www.tradingview.com/symbols/' + crypto
    __browser.get(__url)
    __element = __wait.until(expected_conditions.visibility_of_element_located((By.XPATH,'//*[@id="anchor-page-1"]/div/div[3]/div[1]/div/div/div/div[1]/div[1]')))
    __html = __browser.page_source
    __soup = BeautifulSoup(__html, "lxml")
    try:
        __nome_pregao = __soup.findAll("div", {"class": "tv-symbol-header__long-title-first-text"})[0].text
    except:
        __nome_pregao = ''
    try:
        __cotacao = float(__soup.findAll("div", {"class": "tv-symbol-price-quote__value js-symbol-last"})[0].text)
    except:
        __cotacao = 0
    try:
        __horario = __soup.findAll("span", {"class": "js-symbol-lp-time"})[0].text.replace(')','').replace('(','')
        __horario = datetime.strptime(__horario[:-6], '%b %d %H:%M')
    except:
        __horario = ''
    try:
        __variacao_monetaria = __soup.findAll("span",
                                          {"class": "js-symbol-change tv-symbol-price-quote__change-value"})[0].text
    except:
        __variacao_monetaria = 0
    try:
        __variacao_percentual = __soup.findAll("span",
                                       {"class": "js-symbol-change-pt tv-symbol-price-quote__change-value"})[0].text
    except:
        __variacao_percentual = 0

    if __fecha_browser:
        __browser.close()

    return [crypto, __nome_pregao, __cotacao, __horario, __variacao_monetaria, __variacao_percentual]


def ultimo_pregao(_crypto):
    """
    Busca no site IBOVX a data do último pregão para um crypto

    :param _crypto: código da crypto
    :return: tuple com a data como datetime, data no formato DD/MM/AAAA e a cotação
    """

    url = 'https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=' + _crypto + '&qtdpregoes=1'
    r = requests.get(url, headers=constants.Header.header)
    soup = BeautifulSoup(r.text, 'lxml')
    _tabela = soup.find_all('td')
    try:
        if _tabela[20].text == 'Nº Negócios':
            posicao = 21
        else:
            posicao = 19
        return  (datetime.strptime(_tabela[posicao].text, '%d/%m/%Y'),_tabela[posicao].text)
    except:
        return (None, None)

def cotacao(_crypto, _data):
    """
    Busca no site IBOVX a cotação da crypto na data especificada. Retorna um tuple com data e cotação. Se não houver
    negociação naquela data, retorna a primeira cotação anterior disponível

    :param _crypto: código da crypto
    :param _data: data da cotação

    :return: tuple com a data como datetime, data no formato DD/MM/AAAA e a cotação
    """
    _data = datetime.strptime(_data, '%d/%m/%Y')
    _pregoes = str((datetime.now() - _data).days)
    url = 'https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=' + _crypto + '&qtdpregoes=' + _pregoes
    r = requests.get(url, headers=constants.Header.header)
    soup = BeautifulSoup(r.text, 'lxml')
    _tabela = soup.find_all('td')
    i = len(_tabela)
    _cotacao_anterior = []
    if _tabela[20].text == 'Nº Negócios':
        incremento = 9
    else:
        incremento = 7

    try:
        while i >=0:
            _data_pagina = datetime.strptime(_tabela[i-incremento].text, '%d/%m/%Y')
            _cotacao = float(_tabela[i-incremento+3].text.replace('.','').replace(',','.'))
            if _data_pagina == _data:
                return (_data, _data.strftime('%d/%m/%Y'), _cotacao)
            elif _data_pagina > _data:
                return (_cotacao_anterior)
            _cotacao_anterior = (_data_pagina, _data_pagina.strftime('%d/%m/%Y'), _cotacao)
            i -= incremento
    except:
        return (_cotacao_anterior)


def cotacoes(_crypto, **kwargs):
    """
    Busca no site IBOVX a cotação da crypto na data especificada. Retorna um tuple com data e cotação. Se não houver
    negociação naquela data, retorna a primeira cotação anterior disponível

    :param _crypto: código da crypto
    :param data_inicio: data da primeira cotação, defautl = 01/01/2019
    :param pregoes: quantidade de pregoes retornados = 300

    :return: tuple com a data como datetime, data no formato DD/MM/AAAA e a cotação
    """
    _data = datetime.strptime(_data, '%d/%m/%Y')
    _pregoes = str((datetime.now() - _data).days)
    url = 'https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=' + _crypto + '&qtdpregoes=' + _pregoes
    r = requests.get(url, headers=constants.Header.header)
    soup = BeautifulSoup(r.text, 'lxml')
    _tabela = soup.find_all('td')
    i = len(_tabela)
    _cotacao_anterior = []
    if _tabela[20].text == 'Nº Negócios':
        incremento = 9
    else:
        incremento = 7

    try:
        while i >=0:
            _data_pagina = datetime.strptime(_tabela[i-incremento].text, '%d/%m/%Y')
            _cotacao = float(_tabela[i-incremento+3].text.replace('.','').replace(',','.'))
            if _data_pagina == _data:
                return (_data, _data.strftime('%d/%m/%Y'), _cotacao)
            elif _data_pagina > _data:
                return (_cotacao_anterior)
            _cotacao_anterior = (_data_pagina, _data_pagina.strftime('%d/%m/%Y'), _cotacao)
            i -= incremento
    except:
        return (_cotacao_anterior)


def cotacoes_historicas(crypto='', **kwargs):
    '''
    Carrega as cotações históricas de um crypto

    Args:
        crypto: ticker da crypto
        **kwargs:
            pregoes: quantidade de pregões retornados
            data_inicio: data do pregão mais antigo a ser retornado. Se não houve pregão nesta data, retorna o primeiro
                        pregão após esta data

    Returns:
        caso não seja passado o ticker da crypto (independentemente dos outros parâmetros):
            mensagem: Crypto não pode ser ''.
        caso o argumento data_inicio não seja uma data válida (e não tenha acontecido as situação acima):
            mensagem: Data 'DD/MM/YYYY' é inválida.
        se forem passados ambos os argumentos, vale o número de pregões
        se não for passado nenhum argumento, serão retornados os dados do último pregão

        lista de tuples com os seguintes dados:
            crypto
            data da cotação
            variação de preço percentual
            variação de preço em valor
            cotação
            preço de abertura
            preço mínimo
            preço máximo
            volume financeiro (ordem de grandeza)
            número de negócios


    '''
    if crypto == '':
        return (['Crypto não informado', '','', ''])

    try:
        __browser = kwargs['browser']
        if __browser.__class__.__name__ != 'Browser':
            raise NameError('Objeto passado não é da classe Browser')
        __fecha_browser = False
    except:
        __browser = Browser(clean=True, hide=True)
        __fecha_browser = True


    __param = {}
    for __item in kwargs:
        __param[__item.upper()] = kwargs[__item]
    try:
        pregoes = __param['DIAS']
        __modo_pregoes = True
    except KeyError:
        # data_inicio = datetime.strptime('01/01/2019', '%d/%m/%Y')
        pregoes = 0
        __modo_pregoes = False
    try:
        data_inicio = __param['DATA_INICIO']
        data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y')
    except (KeyError, ValueError):
        if not __modo_pregoes and len(__param) > 0 and __fecha_browser:
            return "Data '" + data_inicio + "' é inválida."
        else:
            data_inicio = ''
            __modo_pregao = True

    if pregoes == 0 and data_inicio == '':
        pregoes = 1
        __modo_pregoes = True
    elif pregoes == 0 and data_inicio != '':
        pregoes = (datetime.now() - data_inicio).days
        __modo_pregoes = False

    __url = 'https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=' + crypto + '&qtdpregoes=' + str(pregoes)
    __browser.get(__url)
    __html = __browser.page_source
    __soup = BeautifulSoup(__html, 'lxml')
    if __soup.text.find('Papel não encontrado ou sem histórico.') >= 0:
        return "Crypto '" + crypto.upper() + "' não encontrado."
    __tabela = __soup.find_all('td')
    __i = len(__tabela)
    __cotacoes = []
    if __tabela[20].text == 'Nº Negócios':
        __incremento = 9
    else:
        __incremento = 7

    while __i >= 0:
        try:
            __data = datetime.strptime(__tabela[__i - __incremento + 0].text, '%d/%m/%Y')
        except ValueError:
            break
        __variacao_perc = funcs.num_ptb2us(__tabela[__i - __incremento + 1].text)
        __variacao_num = funcs.num_ptb2us(__tabela[__i - __incremento + 2].text)
        __cotacao = funcs.num_ptb2us(__tabela[__i - __incremento + 3].text)
        __abertura = funcs.num_ptb2us(__tabela[__i - __incremento + 4].text)
        __minimo = funcs.num_ptb2us(__tabela[__i - __incremento + 5].text)
        __maximo = funcs.num_ptb2us(__tabela[__i - __incremento + 6].text)
        __volumme = funcs.num_ptb2us(__tabela[__i - __incremento + 7].text)
        __negocios = funcs.num_ptb2us(__tabela[__i - __incremento + 8].text)
        if __tabela[__i - __incremento - 1].text.find('bannerresponsivoabaixomenu') > 0:
            __skip = 1
        else:
            __skip = 0
        __cotacoes.append((crypto, __data, __variacao_perc, __variacao_num, __cotacao, __abertura, __minimo, __maximo,
                           __volumme, __negocios))

        __i = __i - __incremento - __skip

    __cotacoes_final = []
    __cotacoes = sorted(__cotacoes, key=lambda x: x[1], reverse=True)
    # __cotacoes.sort(key=takeDate, reverse = True)
    if __modo_pregoes:
        __pregoes_carregados = len(__cotacoes)
        for __id, __linha in enumerate(__cotacoes):
            if __id < pregoes:
                __cotacoes_final.append(__linha)
    else:
        for __linha in __cotacoes:
            if __linha[1] >= data_inicio:
                __cotacoes_final.append(__linha)

    # return "Modo pregões = " + str(__modo_pregoes), "Quantidade de registros = " + str(len(__cotacoes_final)), "Parêmetro pregões = " + str(pregoes), "Última data dos registros = " + str(__cotacoes_final[len(__cotacoes_final)-1][1]), "Parâmetro data de início = " + str(data_inicio)
    if __fecha_browser:
        __browser.close()

    return __cotacoes_final


def volatilidade(crypto='', **kwargs):
    '''
    Busca no site de B3 a volatilidade de um crypto
    args:
        crypto: ticker da crypto
    **kwargs:
        meses=: quantidade de meses da volatilidade (1,3,6,12,99). 99 traz todas a volatilidade de 1, 3, 6 e 12 meses.
               sem este argumento, padrão é 6.
        browser=: instance do browser. se não for passado, uma nova instance será aberta e fechada na saída.


    Returns:
        caso não seja passado o ticker da crypto (independentemente dos outros parâmetros):
            mensagem: 'Crypto não informado'
        caso haja problema com o site da B3:
            tuple [meses informados, meses consultados, erro, url]
        caso nenhum problema:
            tuple [meses informados, meses consultados, desvio padrao, volatilidade anualizada]
'''
    if crypto == '':
        return (['Crypto não informado', '','', ''])

    try:
        __browser = kwargs['browser']
        if __browser.__class__.__name__ != 'Browser':
            raise NameError('Objeto passado não é da classe Browser')
        __fecha_browser = False
    except:
        __browser = Browser(clean=True, hide=True)
        __fecha_browser = True
    try:
        __meses = kwargs['meses']
        __meses_param = __meses
        if '|1|3|6|12|99|'.find('|' + str(__meses) + '|') == -1:
            __meses = 6
    except:
        __meses = 6
    __meses_dict = {
        1: '1mes',
        3: '3meses',
        6: '6meses',
        12: '1ano',
        99: '6meses'
    }
    erros = [
        'Não existem registros para os critérios definidos. Tente novamente.',
        'Sistema indisponível.',
    ]

    __url_root = 'http://bvmf.bmfbovespa.com.br/cias-listadas/volatilidade-cryptos/' \
               'ResumoVolatilidadeCryptos.aspx?metodo=padrao&periodo=xxxxxxxxxx&codigo=' + crypto + '&idioma=pt-br'

    __resultado = []

    __url = __url_root.replace('xxxxxxxxxx', __meses_dict[__meses]).replace('padrao', 'ewma')
    __browser.get(__url)
    __html = __browser.page_source
    __soup = BeautifulSoup(__html, 'lxml')
    __td_list = __soup.find_all('td')
    try:
        __volatilidade_anualizada_ewma = float(__td_list[3].text.replace(',', '.')) / 100
        __desvio_padrao_ewma = __volatilidade_anualizada_ewma / (252 ** .5)
    except:
        for erro in erros:
            if __html.find(erro) != -1:
                __desvio_padrao_ewma = erro
                break
            else:
                __desvio_padrao_ewma = 'Erro desconhecido'
        __volatilidade_anualizada_ewma = ' url: ' + __url


    if __meses == 99:
        for __item in __meses_dict:
            __url = __url_root.replace('xxxxxxxxxx',__meses_dict[__item])
            __browser.get(__url)
            __html = __browser.page_source
            __soup = BeautifulSoup(__html, 'lxml')
            __td_list = __soup.find_all('td')
            try:
                __desvio_padrao = float(__td_list[3].text.replace(',', '.'))
                __volatilidade_anualizada = float(__td_list[4].text.replace(',', '.'))
                __volatilidade_anualizada_calc = __desvio_padrao * (252 ** .5)
            except:
                for erro in erros:
                    if __html.find(erro) != -1:
                        __desvio_padrao = erro
                        break
                    else:
                        __desvio_padrao = 'Erro desconhecido'
                __volatilidade_anualizada = ' url: ' + __url
                __volatilidade_anualizada_calc = ''

            __resultado.append([__meses_param, __item, __desvio_padrao, __volatilidade_anualizada, __volatilidade_anualizada_calc, __desvio_padrao_ewma, __volatilidade_anualizada_ewma])
    else:
        __url = __url_root.replace('xxxxxxxxxx', __meses_dict[__meses])
        __browser.get(__url)
        __html = __browser.page_source
        __soup = BeautifulSoup(__html, 'lxml')
        __td_list = __soup.find_all('td')
        try:
            __desvio_padrao = float(__td_list[3].text.replace(',', '.'))
            __volatilidade_anualizada = float(__td_list[4].text.replace(',', '.'))/100
            __volatilidade_anualizada_calc = __desvio_padrao * (252 ** .5)
        except:
            for erro in erros:
                if __html.find(erro) != -1:
                    __desvio_padrao = erro
                    break
                else:
                    __desvio_padrao = 'Erro desconhecido'
            __volatilidade_anualizada = ' url: ' + __url
            __volatilidade_anualizada_calc = ''

        __resultado.append([__meses_param, __meses, __desvio_padrao, __volatilidade_anualizada, __volatilidade_anualizada_calc, __desvio_padrao_ewma, __volatilidade_anualizada_ewma])

    return __resultado

def cotacoes_historicas_crypto(crypto='', **kwargs):
    '''
    Carrega as cotações históricas de uma cryptomoeda

    Args:
        crypto: ticker da crypto
        **kwargs:
            dias: quantidade de dias retornados
            data_inicio: data mais antiga a ser retornada. Se não houve cotação nesta data, retorna a cotação da 
                        primeira data com cotação após esta

    Returns:
        caso não seja passado o ticker da crypto (independentemente dos outros parâmetros):
            mensagem: Crypto não pode ser ''.
        caso o argumento data_inicio não seja uma data válida (e não tenha acontecido as situação acima):
            mensagem: Data 'DD/MM/YYYY' é inválida.
        se forem passados ambos os argumentos, vale o número de dias
        se não for passado nenhum argumento, será retornada a cotação da última data

        lista de tuples com os seguintes dados:
            crypto
            data da cotação
            variação de preço percentual
            variação de preço em valor
            cotação
            preço de abertura
            preço mínimo
            preço máximo
            volume financeiro (ordem de grandeza)
            número de negócios


    '''
    if crypto == '':
        return (['Crypto não informado', '','', ''])

    try:
        __browser = kwargs['browser']
        if __browser.__class__.__name__ != 'Browser':
            raise NameError('Objeto passado não é da classe Browser')
        __fecha_browser = False
    except:
        __browser = Browser(clean=True, hide=True)
        __fecha_browser = True


    __param = {}
    for __item in kwargs:
        __param[__item.upper()] = kwargs[__item]
    try:
        pregoes = __param['DIAS']
        __modo_pregoes = True
    except KeyError:
        # data_inicio = datetime.strptime('01/01/2019', '%d/%m/%Y')
        pregoes = 0
        __modo_pregoes = False
    try:
        data_inicio = __param['DATA_INICIO']
        data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y')
    except (KeyError, ValueError):
        if not __modo_pregoes and len(__param) > 0 and __fecha_browser:
            return "Data '" + data_inicio + "' é inválida."
        else:
            data_inicio = ''
            __modo_pregao = True

    if pregoes == 0 and data_inicio == '':
        pregoes = 1
        __modo_pregoes = True
    elif pregoes == 0 and data_inicio != '':
        pregoes = (datetime.now() - data_inicio).days
        __modo_pregoes = False

    __url = 'https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=' + crypto + '&qtdpregoes=' + str(pregoes)
    __browser.get(__url)
    __html = __browser.page_source
    __soup = BeautifulSoup(__html, 'lxml')
    if __soup.text.find('Papel não encontrado ou sem histórico.') >= 0:
        return "Crypto '" + crypto.upper() + "' não encontrado."
    __tabela = __soup.find_all('td')
    __i = len(__tabela)
    __cotacoes = []
    if __tabela[20].text == 'Nº Negócios':
        __incremento = 9
    else:
        __incremento = 7

    while __i >= 0:
        try:
            __data = datetime.strptime(__tabela[__i - __incremento + 0].text, '%d/%m/%Y')
        except ValueError:
            break
        __variacao_perc = funcs.num_ptb2us(__tabela[__i - __incremento + 1].text)
        __variacao_num = funcs.num_ptb2us(__tabela[__i - __incremento + 2].text)
        __cotacao = funcs.num_ptb2us(__tabela[__i - __incremento + 3].text)
        __abertura = funcs.num_ptb2us(__tabela[__i - __incremento + 4].text)
        __minimo = funcs.num_ptb2us(__tabela[__i - __incremento + 5].text)
        __maximo = funcs.num_ptb2us(__tabela[__i - __incremento + 6].text)
        __volumme = funcs.num_ptb2us(__tabela[__i - __incremento + 7].text)
        __negocios = funcs.num_ptb2us(__tabela[__i - __incremento + 8].text)
        if __tabela[__i - __incremento - 1].text.find('bannerresponsivoabaixomenu') > 0:
            __skip = 1
        else:
            __skip = 0
        __cotacoes.append((crypto, __data, __variacao_perc, __variacao_num, __cotacao, __abertura, __minimo, __maximo,
                           __volumme, __negocios))

        __i = __i - __incremento - __skip

    __cotacoes_final = []
    __cotacoes = sorted(__cotacoes, key=lambda x: x[1], reverse=True)
    # __cotacoes.sort(key=takeDate, reverse = True)
    if __modo_pregoes:
        __pregoes_carregados = len(__cotacoes)
        for __id, __linha in enumerate(__cotacoes):
            if __id < pregoes:
                __cotacoes_final.append(__linha)
    else:
        for __linha in __cotacoes:
            if __linha[1] >= data_inicio:
                __cotacoes_final.append(__linha)

    # return "Modo pregões = " + str(__modo_pregoes), "Quantidade de registros = " + str(len(__cotacoes_final)), "Parêmetro pregões = " + str(pregoes), "Última data dos registros = " + str(__cotacoes_final[len(__cotacoes_final)-1][1]), "Parâmetro data de início = " + str(data_inicio)
    if __fecha_browser:
        __browser.close()

    return __cotacoes_final