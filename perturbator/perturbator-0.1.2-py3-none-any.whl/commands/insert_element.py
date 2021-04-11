import click
from src.perturbator.support_modules.perturbator import add_new_element_to_flow, validate_flow_presence_in_file

@click.command()
@click.option('--insert-to', required=True, type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              help='BPMN File Path in which element has to be inserted')
@click.option('--element-type', required=True,
              help='Type of element to be inserted')
@click.option('--insert-at', required=True,
              help='ID of the FLOW where the element has to be inserted' )
@click.option('--output-file', required=True, type=click.Path(exists=False, dir_okay=False,
              writable=True, resolve_path=True), help="Path of BPMN file in which to output")
def insert_element(insert_to, element_type, insert_at, output_file):
    if validate_flow_presence_in_file(insert_to, insert_at) is False:
        click.echo('Flow does not exist in the process where you are trying to insert')
        return
    add_new_element_to_flow(insert_to, element_type, insert_at, output_file)
