"""
Scripts do console
"""
from kt_pullback import kt_pullback
from kt_pullback import __version__
import click


@click.command()
@click.argument("preco_final", type=float, required=False)
@click.argument("preco_inicial", type=float, required=False)
@click.option("--version", is_flag=True, help="Exibe a versao")
def cli(preco_final, preco_inicial, version):
    """Calcula retracoes de uma perna."""
    if version:
        click.echo("kt-pullback %s" % __version__)
        return 0
    if not preco_final:
        click.echo("Usage: pb [OPTIONS] [PRECO_FINAL] [PRECO_INICIAL]")
        return 0
    tamanho = kt_pullback.tamanho_perna(preco_final, preco_inicial)
    metade = kt_pullback.metade_perna(tamanho)
    terco = kt_pullback.terco_perna(tamanho)
    recuo1 = kt_pullback.retracao_um_terco(preco_final, terco)
    recuo2 = kt_pullback.retracao_metade(preco_final, metade)
    recuo3 = kt_pullback.retracao_dois_tercos(preco_final, terco)
    click.echo("%.2f" % recuo1)
    click.echo("%.2f" % recuo2)
    click.echo("%.2f" % recuo3)
