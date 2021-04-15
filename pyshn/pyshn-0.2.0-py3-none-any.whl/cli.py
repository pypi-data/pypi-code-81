from pyshn.cpf import cpf as _cpf, CpfError
from pyshn.cnpj import cnpj as _cnpj, CnpjError
import pyshn
import click

@click.group()
@click.version_option(version=pyshn.__version__)
def main():
    pass

@main.command()
@click.argument('number', 
    nargs=1, 
    type=str
)
@click.option('--format', 'format_spec',
    type=click.Choice(['s', 'N', 'n']),
    default='s',
    help="""s: the default format.                                  
    N: the new format (displayed in the latest documents).         
    n: the numeric format (show only digits)."""
)
@click.option('--generate',
    is_flag=True,
    default=False,
    help="Generate the checksum."
)
@click.option('--no-validate', 
    is_flag=True, 
    default=False,
    help="Don't validate the CPF number."
)
def cpf(number:str, generate:bool, no_validate:bool, format_spec:str):
    """
    Format, validate or generate CPF's numbers.
    """
    try:
        if number.isnumeric():
            number=int(number)

        if format_spec == 's':
            format_spec = ''

        result = _cpf(number, generate=generate, validate=False)
        output = format(result, format_spec)

        if not generate and no_validate == False:
            output += " "
            output += "(valid)" if result else "(invalid)"

        click.echo(output)
    except CpfError as e:
        click.echo(message=f"pyshn: {e}")

@main.command()
@click.argument('number', 
    nargs=1, 
    type=str
)
@click.option('--format', 'format_spec',
    type=click.Choice(['s', 'N', 'n']),
    default='s',
    help="""s: the default format.                                  
    N: the new format (displayed in the latest documents).         
    n: the numeric format (show only digits)."""
)
@click.option('--generate',
    is_flag=True,
    default=False,
    help="Generate the checksum."
)
@click.option('--no-validate', 
    is_flag=True, 
    default=False,
    help="Don't validate the CNPJ number."
)
def cnpj(number:str, generate:bool, no_validate:bool, format_spec:str):
    """
    Format, validate or generate CNPJ's numbers.
    """
    try:
        if number.isnumeric():
            number=int(number)
        
        if format_spec == 's':
            format_spec = ''
        
        result = _cnpj(number, generate=generate, validate=False)
        output = format(result, format_spec)

        if not generate and no_validate == False:
            output += " "
            output += "(valid)" if result else "(invalid)"
        
        click.echo(output)
    except CnpjError as e:
        click.echo(message=f"pyshn: {e}")
