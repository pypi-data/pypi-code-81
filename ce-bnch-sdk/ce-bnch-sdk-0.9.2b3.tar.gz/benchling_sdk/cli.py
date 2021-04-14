import typer

from benchling_sdk.benchbots.cli import benchbots_cli

cli = typer.Typer()
cli.add_typer(benchbots_cli, name="benchbot")

if __name__ == "__main__":
    cli()
