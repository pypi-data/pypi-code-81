import click
from src.perturbator.support_modules.perturbator import serial_insert_process, validate_flow_presence_in_file


@click.command()
@click.option('--insert-to', required=True, type=click.Path(exists=True, dir_okay=False),
              help='BPMN File Path in which process has to be inserted')
@click.option('--insert-from', required=True, type=click.Path(exists=True, dir_okay=False, writable=False),
              help='BPMN File Path from which process has to be inserted')
@click.option('--output-file', required=True, type=click.Path(exists=False, dir_okay=False, writable=True),
              help="Path of BPMN file in which to output")
@click.option('--insert-at', required=True,
              help='ID of the FLOW where the process has to be inserted' )
def insert_process_fragment_serial(insert_to, insert_from, insert_at, output_file):
    if validate_flow_presence_in_file(insert_to, insert_at) is False:
        click.echo('Flow does not exist in the process where you are trying to insert')
        return
    serial_insert_process(insert_to, insert_from, insert_at, output_file)
