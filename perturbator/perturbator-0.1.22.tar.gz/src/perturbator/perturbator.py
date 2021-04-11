import click

from .commands import generate_new_element, insert_process_fragment_serial, \
    insert_process_fragment_conditional, insert_process_fragment_parallel, delete_process_fragment, insert_element, \
    delete_element, execute_from_file


@click.group(help="Business Process Model Perturbator")
def cli():
    pass


cli.add_command(generate_new_element.generate_new_element)
cli.add_command(insert_process_fragment_serial.insert_process_fragment_serial)
cli.add_command(insert_process_fragment_conditional.insert_process_fragment_conditional)
cli.add_command(insert_process_fragment_parallel.insert_process_fragment_parallel)
cli.add_command(delete_process_fragment.delete_process_fragment)
cli.add_command(insert_element.insert_element)
cli.add_command(delete_element.delete_element)
cli.add_command(execute_from_file.execute_from_file)


def main():
    cli()
