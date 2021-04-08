"""
Scripts do console
"""
from kt_line import kt_line
from kt_line import __version__
import click


@click.command()
@click.argument("preco-a", type=float, required=False)
@click.argument("preco-b", type=float, required=False)
@click.option("--version", is_flag=True, help="Exibe a versao")
def cli(preco_a, preco_b, version):
    """Calcula proximo preco da linha de canal."""
    if version:
        click.echo("kt-line %s" % __version__)
        return 0
    if not preco_a:
        click.echo("Usage: l [OPTIONS] [PRECO-A] [PRECO-B]")
        return 0
    preco_c = kt_line.line(preco_a, preco_b)
    click.echo(preco_c)
    return 0


if __name__ == "__main__":
    cli()
