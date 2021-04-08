"""
Arquivo de definições
"""


def osc(preco_final, preco_inicial):
    "Calcula a variação percentual entre dois precos." ""
    osc_absoluta = preco_final - preco_inicial
    osc_percentual = osc_absoluta / preco_inicial * 100
    return "%.1f%%" % osc_percentual
