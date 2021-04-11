import click

from ..support_modules.perturbator import skip_element


@click.command()
@click.option('--delete-from', required=True, type=click.Path(exists=True, dir_okay=False),
              help='BPMN File Path from which element has to be skipped')
@click.option('--element-id', required=True,
              help='ID of Element to be deleted')
@click.option('--output-file', required=True, type=click.Path(exists=False, dir_okay=False, writable=True),
              help="Path of BPMN file in which to output")
def delete_element(delete_from, element_id, output_file):
    skip_element(delete_from, element_id, output_file)
