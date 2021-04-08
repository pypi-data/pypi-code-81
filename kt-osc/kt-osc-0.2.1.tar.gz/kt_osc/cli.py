"""
Scripts do console
"""
from kt_osc import kt_osc
from kt_osc import __version__
import click


@click.command()
@click.argument("preco-final", type=float, required=False)
@click.argument("preco-inicial", type=float, required=False)
@click.option("--version", is_flag=True, help="Exibe a versao")
def cli(preco_final, preco_inicial, version):
    """Calcula oscilacao entre preco final e preco inicial."""
    if version:
        click.echo("kt-osc %s" % __version__)
        return 0
    if not preco_final:
        click.echo("Usage: osc [OPTIONS] [PRECO-FINAL] [PRECO-INCIAL]")
        return 0
    click.echo(kt_osc.osc(preco_final, preco_inicial))
    return 0


if __name__ == "__main__":
    cli()
