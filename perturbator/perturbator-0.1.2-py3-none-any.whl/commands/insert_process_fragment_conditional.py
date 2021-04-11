import click
from src.perturbator.support_modules.perturbator import branch_insert_process, validate_flow_presence_in_file


@click.command()
@click.option('--insert-to', required=True, type=click.Path(exists=True, dir_okay=False),
              help='BPMN File Path in which process has to be inserted')
@click.option('--insert-from', required=True, type=click.Path(exists=True, dir_okay=False, writable=False),
              help='BPMN File Path from which process has to be inserted')
@click.option('--output-file', required=True, type=click.Path(exists=False, dir_okay=False, writable=True),
              help="Path of BPMN file in which to output")
@click.option('--branch-start', required=True,
              help='ID of the FLOW where the branching starts')
@click.option('--branch-end', required=True,
              help='ID of the FLOW where the branching starts')
def insert_process_fragment_conditional(insert_to, insert_from, output_file, branch_start, branch_end):
    if validate_flow_presence_in_file(insert_to, branch_start) is False:
        click.echo('Starting Branch Flow does not exist in the process where you are trying to insert')
        return

    if validate_flow_presence_in_file(insert_to, branch_end) is False:
        click.echo('Ending Branch Flow does not exist in the process where you are trying to insert')
        return

    branch_insert_process(insert_to, insert_from, branch_start, branch_end, output_file, True)
