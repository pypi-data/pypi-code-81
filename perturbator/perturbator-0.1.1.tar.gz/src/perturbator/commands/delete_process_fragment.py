import click
from src.perturbator.support_modules.perturbator import skip_process_fragment, validate_flow_presence_in_file


@click.command()
@click.option('--delete-from', required=True, type=click.Path(exists=True, dir_okay=False, writable=False),
              help='BPMN File Path from which process fragment has to deleted')
@click.option('--output-file', required=True, type=click.Path(exists=False, dir_okay=False, writable=True),
              help="Path of BPMN file in which to output")
@click.option('--branch-start', required=True,
              help='ID of the FLOW where the branching starts')
@click.option('--branch-end', required=True,
              help='ID of the FLOW where the branching starts')
def delete_process_fragment(delete_from, output_file, branch_start, branch_end):
    if validate_flow_presence_in_file(delete_from, branch_start) is False:
        click.echo('Starting Branch Flow does not exist in the process fragment from which you try to delete')
        return

    if validate_flow_presence_in_file(delete_from, branch_end) is False:
        click.echo('Ending Branch Flow does not exist in the process fragment until which you try to delete')
        return

    skip_process_fragment(delete_from, output_file, branch_start, branch_end)
