import click
from src.perturbator.language_parser import language_model_generator
from os.path import expanduser

from src.perturbator.commands.insert_element import insert_element
from src.perturbator.commands.delete_element import delete_element
from src.perturbator.commands.insert_process_fragment_serial import insert_process_fragment_serial
from src.perturbator.commands.insert_process_fragment_parallel import insert_process_fragment_parallel
from src.perturbator.commands.insert_process_fragment_conditional import insert_process_fragment_conditional
from src.perturbator.commands.delete_process_fragment import delete_process_fragment


def cname(o):
    return o.__class__.__name__


def prepare_file_argument(path):
    return expanduser(path)


def prepare_alternate_branch_fields(command):
    branchStart = command.startingFlow
    branchEnd = command.endingFlow

    return [branchStart, branchEnd];


def prepare_branch_insertion_fields(command):
    insertTo = prepare_file_argument(command.path)
    insertFrom = prepare_file_argument(command.extractPath)
    outputFile = prepare_file_argument(command.outputPath)
    [branchStart, branchEnd] = prepare_alternate_branch_fields(command)

    return [insertTo, insertFrom, outputFile, branchStart, branchEnd];


@click.command()
@click.option('--command-file', required=True, type=click.Path(exists=True, dir_okay=False),
              help='BPMN File Path from which command has to be executed')
@click.pass_context
def execute_from_file(ctx, command_file):
    commands = language_model_generator.retrieve_commands(command_file)

    for command in commands:
        if cname(command) == 'InsertElementCommand':
            insertTo = prepare_file_argument(command.path)
            elementType = command.elementType
            insertAt = command.flow
            outputFile = prepare_file_argument(command.outputPath)

            ctx.invoke(insert_element, insert_to=insertTo, element_type=elementType,
                       insert_at=insertAt, output_file=outputFile)
        elif cname(command) == 'DeleteElementCommand':
            deleteFrom = prepare_file_argument(command.path)
            elementId = command.elementId
            outputFile = prepare_file_argument(command.outputPath)

            ctx.invoke(delete_element, delete_from=deleteFrom, element_id=elementId, output_file=outputFile)
        elif cname(command) == 'InsertSerialCommand':
            insertTo = prepare_file_argument(command.path)
            insertFrom = prepare_file_argument(command.extractPath)
            insertAt = command.flow
            outputFile = prepare_file_argument(command.outputPath)

            ctx.invoke(insert_process_fragment_serial, insert_to=insertTo, insert_from=insertFrom,
                       insert_at=insertAt, output_file=outputFile)
        elif cname(command) == 'InsertParallelCommand':
            [insertTo, insertFrom, outputFile, branchStart, branchEnd] = prepare_branch_insertion_fields(command)

            ctx.invoke(insert_process_fragment_parallel, insert_to=insertTo, insert_from=insertFrom,
                       output_file=outputFile, branch_start=branchStart, branch_end=branchEnd)
        elif cname(command) == 'InsertConditionalCommand':
            [insertTo, insertFrom, outputFile, branchStart, branchEnd] = prepare_branch_insertion_fields(command)

            ctx.invoke(insert_process_fragment_conditional, insert_to=insertTo, insert_from=insertFrom,
                       output_file=outputFile, branch_start=branchStart, branch_end=branchEnd)
        elif cname(command) == 'DeleteFragmentCommand':
            deleteFrom = prepare_file_argument(command.path)
            outputFile = prepare_file_argument(command.outputPath)
            [branchStart, branchEnd] = prepare_alternate_branch_fields(command)

            ctx.invoke(delete_process_fragment, delete_from=deleteFrom, output_file=outputFile, branch_start=branchStart, branch_end=branchEnd)

