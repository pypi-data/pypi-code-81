import click
from src.perturbator.support_modules.perturbator import generate_element

@click.command()
@click.option('--element-tag', help='Tag of element, e.g. exclusiveGateway, task', required=True)
@click.option('--element-id', help='Id of the element you want to generate', required=True)
def generate_new_element(element_tag, element_id):
    element = generate_element(element_tag, element_id)
    click.echo('Element generated with id %s!' % element.attrib['id'])

