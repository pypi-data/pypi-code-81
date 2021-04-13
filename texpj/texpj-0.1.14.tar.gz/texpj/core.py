#!/usr/bin/env python3
import click
import sys
import os
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """
    Utilidad para manejo de plantillas de latex por consola.

    Utilice:

    $ texpj comando -h

    Para obtener una mayor información sobre el comando.
    """
    print('** Dame chance jajaja sólo aparté el nombre **')
    #print(sys.argv)
    #os.system('ls')

@main.command()
@click.argument('template')
@click.argument('alias')
@click.option('--url/--no-url', default=False, help="indica si es un url")
def install(template, alias, url):
    """
    Instala el TEMPLATE de forma local y lo regitra como ALIAS.

    Descarga un repositorio con el comando git. 'user/repo-name' bastará si es un 
    repositorio de Github sino
    puede utilizar un url activando la opción --url.
    
    \b
    Ejemplo:
    $ texpj install BenyaminGaleano/report
    $ texpj install https://github.com/BenyaminGaleano/report.git --url
    """
    print(f'Falta implementación, {template} {alias} url:{url}')


@main.command()
@click.argument('alias')
def update(alias):
    """
    Actualiza el template identificado con el ALIAS.
    """
    print(f'Falta implementación, {alias}')


@main.command()
@click.argument('directory')
@click.argument('alias')
def add(directory, alias):
    """
    Registra DIRECTORY como una plantilla de latex y lo identifica con ALIAS.

    \b
    $ texpj add . elec_doc
    $ texpj add reporte report
    """
    print(f'Falta implementación, {alias}')


@main.command()
@click.argument('alias')
@click.argument('name')
@click.option('--directory', '-d', help="directorio base")
def create(alias, directory):
    """
    Crea una copia del template registrado como ALIAS en la posición actual o en 
    el directorio indicado con -d con el nombre NAME.

    \b
    $ texpj create report lab1
    $ texpj create report lab1 -d ~/documentos/latex
    """
    print(f'Falta implementación, {alias}, {directory}')

if __name__ == "__main__":
    main()

