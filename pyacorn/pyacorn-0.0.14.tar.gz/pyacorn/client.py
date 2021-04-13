# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from jinja2 import Environment, PackageLoader
from urllib.parse import quote

import base64
import click
import commentjson
import getpass
import io
import json
import netrc
import os
import pickle
import platform
import pprint
import pyfiglet
import requests
import sys
import textwrap
import uuid
import binascii
import zipfile
import decimal


class VersionType(click.ParamType):
    name = "version"

    def convert(self, value, param, ctx):
        try:
            return decimal.Decimal(value)
        except decimal.InvalidOperation:
            self.fail(f"{value!r} is not a valid version", param, ctx)


@click.group()
def cli():
    """The python command line tool for acorn"""
    pass

@cli.command()
@click.option('--username', prompt='enter username')
@click.option('--password', prompt='enter password', hide_input=True)
def login(username, password):
    """Login to acorn (stores temporary credentials in netrc)"""
    splash('log in')

    filename, _ = prepare_credentials()
    click.echo('contacting server...\t', nl=False)
    with requests.Session() as session:
        r = session.post('{}/auth/login'.format(ACORN), auth=(username, password))
        if not r.ok:
            sys.exit('[FAIL] {} error: login attempt failed'.format(r.status_code))

        cookies = base64.b64encode(pickle.dumps(session.cookies))
        payload = r.json()
    click.echo('[OK]')

    click.echo('storing credentials...\t', nl=False)
    with open(filename, 'r+') as f:
        data = f.read()
        try:
            idx = data.index('machine {} login '.format(ACORN))
            f.seek(idx)
            line = f.readline()
            f.seek(idx)
            overwritten = f.write(data[idx + len(line):])
            f.truncate(idx + overwritten)
        except ValueError:
            pass

        f.write('machine {} login {} password {}\n'.format(ACORN, cookies.decode(), payload['refresh']))
        click.echo('[SUCCESS]')

@cli.command()
def logout():
    """Logout from acorn (clears any stored credentials)"""
    splash('log out')

    click.echo('checking netrc...\t', nl=False)
    filename = os.path.join(os.path.expanduser('~'), '_netrc' if WINDOWS else '.netrc')
    if not os.path.isfile(filename):
        sys.exit('[FAIL] not logged in.')
    click.echo('[OK]')

    click.echo('searching for data...\t', nl=False)
    with open(filename, 'r+') as f:
        data = f.read()
        try:
            idx = data.index('machine {} login '.format(ACORN))
            f.seek(idx)
            line = f.readline()
            f.seek(idx)
            overwritten = f.write(data[idx + len(line):])
            f.truncate(idx + overwritten)
            click.echo('[OK] Log out successful')
        except ValueError:
            sys.exit('[FAIL] not logged in.')

@cli.command(name='list')
@click.option('--query', '-q')
def list_projects(query):
    """ Browse through all available projects """
    url = '{}/acorn/create/view/project'.format(ACORN)
    params = {}
    if query:
        params['$search'] = query

    with load_session() as session:
        while True:
            r = session.get(url, params=params)
            if not r.ok:
                click.echo(pprint.pprint(r.json()))
                sys.exit('fetching page...\t[FAIL] {} error: unable to list projects'.format(r.status_code))

            payload = r.json()
            for row in payload['rows']:
                description = textwrap.fill(
                    row['description'],
                    width=70,
                    subsequent_indent='\t',
                    initial_indent='     >\t')

                click.echo('[{}] {}\n'.format(uuid.UUID(row['id']).hex, row['name']))
                click.echo(description)
                click.echo()

            token = payload['token']
            if token:
                params['$skiptoken'] = token
                click.pause('press any key for next page ...'.rjust(80))
                url = '{}/acorn/create/view/project?$skiptoken={}'.format(ACORN, token)
            else:
                break

@cli.command(name='grow')
@click.argument('project')
@click.option('path', '--dir', '-d', type=click.Path())
@click.option('--version', type=VersionType())
@click.option('--branch', default="master")
@click.option('--vscode', is_flag=True)
@click.option('--force-project', is_flag=True)
@click.option('--runtime', '-r', default="python3")
def generate_project(project, path, version, branch, vscode, force_project, runtime):
    """ Expand a new or existing project """
    if path:
        splash('grow project in {}'.format(path))
    else:
        splash('grow new project')

    click.echo('analysing project...\t', nl=False)
    try:
        projectid = uuid.UUID(hex=project)
    except ValueError:
        sys.exit('[FAIL] invalid project identifier')
    click.echo('[OK]')
    
    with load_session() as session:
        click.echo('fetching metadata...\t', nl=False)
        r = session.get('{}/acorn/create/context/project?project_id={}'.format(ACORN, projectid))
        if not r.ok:
            sys.exit('[FAIL] unable to download metadata')
        click.echo('[OK]')

        metadata = r.json()
        if path:
            click.echo('checking directory...\t', nl=False)
            target = os.path.abspath(path)
            os.makedirs(target, exist_ok=True)
            if not os.path.isdir(target):
                sys.exit('[FAIL] "{}" does not exist or is not a directory.'.format(target))
            click.echo('[OK]')
        else:
            click.echo('checking directory...\t', nl=False)
            target = os.path.join(os.getcwd(), metadata['name'])
            try:
                os.makedirs(target)
            except FileExistsError:
                sys.exit('[FAIL] project already exists at {}.'.format(target))
            click.echo('[OK]')

        manifest = os.path.join(target, '.acorn')
        if os.path.isfile(manifest):
            click.echo('cleaning directory...\t', nl=False)
            do_clean(target, manifest)
        
        config = os.path.join(target, metadata['name'] + '.cfg')
        if not os.path.exists(config):
            with open(config, 'w') as f:
                f.write(CONFIG.format(cwd=target, issuer=uuid.uuid1(), secret=token_hex(8)))

        click.echo('downloading project...\t', nl=False)
        params = {
            'branch': branch if version is None else 'final',
        }
        if version:
            params['version'] = version
        if force_project:
            params['format'] = 'project'
        if runtime:
            params['runtime'] = runtime

        r = session.get(
            '{}/acorn/create/context/project/{}/view/development'.format(ACORN, projectid),
            params=params)
        if r.status_code == 404:
            sys.exit('[FAIL] {} error: requested artifact not found'.format(r.status_code))
        elif not r.ok:
            sys.exit('[FAIL] {} error: unable to download project'.format(r.status_code))
        click.echo('[OK]')
        zf = zipfile.ZipFile(io.BytesIO(r.content))
    
    click.echo('creating manifest...\t', nl=False)
    acorn = {
        'generated': zf.read('.generated').decode().strip().splitlines(),
        'editable': zf.read('.editable').decode().strip().splitlines(),
    }
    with open(manifest, 'w') as f:
        json.dump(acorn, f, indent=2)
    click.echo('[OK]')
    
    directories = set()
    ignored = {}
    click.echo('growing leaves...\t', nl=False)
    for filename in acorn['generated']:
        parts = filename.split('/')
        suffix = filename[len(parts[0])+1:]
        if parts[0] in ignored:
            ignored[parts[0]].append(suffix)
        else:
            ignored[parts[0]] = [suffix]

        fqn = os.path.join(target, *parts)
        parent = os.path.dirname(fqn)
        if parent not in directories:
            directories.add(parent)
            os.makedirs(parent, exist_ok=True)

        zf.extract(filename, path=target)
    click.echo('[OK] {} leaves sprouted'.format(len(acorn['generated'])))

    click.echo('checking roots...\t', nl=False)
    for filename in acorn['editable']:
        fqn = os.path.join(target, *filename.split('/'))
        parent = os.path.dirname(fqn)
        if parent not in directories:
            directories.add(parent)
            os.makedirs(parent, exist_ok=True)

        if not os.path.exists(fqn):
            zf.extract(filename, path=target)
    click.echo('[OK] {} roots intact'.format(len(acorn['editable'])))
    
    click.echo('finalizing growth...\t', nl=False)
    for directory, files in ignored.items():
        parent = os.path.join(target, directory)
        if os.path.isdir(parent):
            with open(os.path.join(parent, '.gitignore'), 'w') as f:
                f.write('\n'.join(files))

    if vscode:
        configure_vscode(metadata['name'], target)

    click.echo('[SUCCESS]')

@cli.command(name='graft')
@click.argument('project')
@click.argument('path', type=click.Path())
@click.option('--version', type=VersionType())
@click.option('--branch', default="master")
@click.option('--runtime', '-r', default="python3")
def generate_client(project, path, version, branch, runtime):
    """ Expand a new or existing client """
    if path:
        splash('graft client in {}'.format(path))
    else:
        splash('graft client here')

    click.echo('analysing project...\t', nl=False)
    try:
        projectid = uuid.UUID(hex=project)
    except ValueError:
        sys.exit('[FAIL] invalid project identifier')
    click.echo('[OK]')
    
    with load_session() as session:
        click.echo('fetching metadata...\t', nl=False)
        r = session.get('{}/acorn/create/context/project?project_id={}'.format(ACORN, projectid))
        if not r.ok:
            sys.exit('[FAIL] unable to download metadata')
        click.echo('[OK]')

        if path:
            click.echo('checking directory...\t', nl=False)
            target = os.path.abspath(path)
            if not os.path.isdir(target):
                sys.exit('[FAIL] "{}" does not exist or is not a directory.'.format(target))
            click.echo('[OK]')
        else:
            target = os.path.abspath(path)

        manifest = os.path.join(target, '.acorn')
        if os.path.isfile(manifest):
            click.echo('cleaning directory...\t', nl=False)
            do_clean(target, manifest)

        click.echo('downloading client...\t', nl=False)
        params = {
            'branch': branch if version is None else 'final',
            'format': 'client',
        }
        if version:
            params['version'] = version
        if runtime:
            params['runtime'] = runtime

        r = session.get(
            '{}/acorn/create/context/project/{}/view/development'.format(ACORN, projectid),
            params=params)
        if r.status_code == 404:
            sys.exit('[FAIL] {} error: requested artifact not found'.format(r.status_code))
        elif not r.ok:
            sys.exit('[FAIL] {} error: unable to download project'.format(r.status_code))
        click.echo('[OK]')
        zf = zipfile.ZipFile(io.BytesIO(r.content))
    
    click.echo('creating manifest...\t', nl=False)
    acorn = {
        'generated': zf.read('.generated').decode().strip().splitlines(),
        'editable': zf.read('.editable').decode().strip().splitlines(),
    }
    with open(manifest, 'w') as f:
        json.dump(acorn, f, indent=2)
    click.echo('[OK]')
    
    directories = set()
    ignored = {}
    click.echo('grafting leaves...\t', nl=False)
    for filename in acorn['generated']:
        parts = filename.split('/')
        suffix = filename[len(parts[0])+1:]
        if parts[0] in ignored:
            ignored[parts[0]].append(suffix)
        else:
            ignored[parts[0]] = [suffix]

        fqn = os.path.join(target, *parts)
        parent = os.path.dirname(fqn)
        if parent not in directories:
            directories.add(parent)
            os.makedirs(parent, exist_ok=True)

        zf.extract(filename, path=target)
    click.echo('[OK] {} leaves transfered'.format(len(acorn['generated'])))

    click.echo('checking roots...\t', nl=False)
    for filename in acorn['editable']:
        fqn = os.path.join(target, *filename.split('/'))
        parent = os.path.dirname(fqn)
        if parent not in directories:
            directories.add(parent)
            os.makedirs(parent, exist_ok=True)

        if not os.path.exists(fqn):
            zf.extract(filename, path=target)
    click.echo('[OK] {} roots shifted'.format(len(acorn['editable'])))
    
    click.echo('finalizing growth...\t', nl=False)
    for directory, files in ignored.items():
        parent = os.path.join(target, directory)
        if os.path.isdir(parent):
            with open(os.path.join(parent, '.gitignore'), 'w') as f:
                f.write('\n'.join(files))

    click.echo('[SUCCESS]')


@cli.command(name='sprout')
@click.argument('project')
@click.argument('token')
@click.argument('path', type=click.Path())
@click.option('--version', type=VersionType())
@click.option('--branch', default="master")
@click.option('--no-metadata', is_flag=True)
def generate_target(project, token, path, version, branch, no_metadata):
    """ Expand from a public target """
    if path:
        splash('sprout in {}'.format(path))
    else:
        splash('sprout here')
    
    with requests.Session() as session:
        if path:
            click.echo('checking directory...\t', nl=False)
            target = os.path.abspath(path)
            os.makedirs(target, exist_ok=True)
            if not os.path.isdir(target):
                sys.exit('[FAIL] "{}" does not exist or is not a directory.'.format(target))
            click.echo('[OK]')
        else:
            target = os.path.abspath(path)

        manifest = os.path.join(target, '.acorn')
        if os.path.isfile(manifest):
            click.echo('cleaning directory...\t', nl=False)
            do_clean(target, manifest)
        
        click.echo('downloading code...\t', nl=False)
        params = {
            'token': quote(token),
            'branch': branch if version is None else 'final',
        }
        if version:
            params['version'] = version

        r = session.get(
            '{}/acorn/consumer/context/module/{}/view/generate'.format(
                ACORN,
                quote(project)),
            params=params)
        if r.status_code == 404:
            sys.exit('[FAIL] {} error: requested artifact not found'.format(r.status_code))
        elif not r.ok:
            sys.exit('[FAIL] {} error: unable to download project'.format(r.status_code))
        click.echo('[OK]')
        zf = zipfile.ZipFile(io.BytesIO(r.content))
    
    click.echo('creating manifest...\t', nl=False)
    acorn = {
        'generated': zf.read('.generated').decode().strip().splitlines(),
        'editable': zf.read('.editable').decode().strip().splitlines(),
    }
    if no_metadata:
        click.echo('[SKIPPED]')
    else:
        with open(manifest, 'w') as f:
            json.dump(acorn, f, indent=2)
        click.echo('[OK]')
    
    directories = set()
    ignored = {}
    click.echo('grafting leaves...\t', nl=False)
    for filename in acorn['generated']:
        parts = filename.split('/')
        if no_metadata and parts[-1].startswith('.'):
            continue

        suffix = filename[len(parts[0])+1:]
        if parts[0] in ignored:
            ignored[parts[0]].append(suffix)
        else:
            ignored[parts[0]] = [suffix]

        fqn = os.path.join(target, *parts)
        parent = os.path.dirname(fqn)
        if parent not in directories:
            directories.add(parent)
            os.makedirs(parent, exist_ok=True)

        zf.extract(filename, path=target)
    click.echo('[OK] {} leaves transfered'.format(len(acorn['generated'])))

    click.echo('checking roots...\t', nl=False)
    for filename in acorn['editable']:
        fqn = os.path.join(target, *filename.split('/'))
        parent = os.path.dirname(fqn)
        if parent not in directories:
            directories.add(parent)
            os.makedirs(parent, exist_ok=True)

        if not os.path.exists(fqn):
            zf.extract(filename, path=target)
    click.echo('[OK] {} roots shifted'.format(len(acorn['editable'])))
    
    click.echo('finalizing growth...\t', nl=False)
    if not no_metadata:
        for directory, files in ignored.items():
            parent = os.path.join(target, directory)
            if os.path.isdir(parent):
                with open(os.path.join(parent, '.gitignore'), 'w') as f:
                    f.write('\n'.join(files))

    click.echo('[SUCCESS]')

@cli.command(name='clean')
@click.option('path', '--dir', '-d', type=click.Path())
def clean_project(path):
    """ Clean all generated files from the project """
    target = path if path else os.getcwd()
    splash('clean {}'.format(target))

    click.echo('checking directory...\t', nl=False)
    if not os.path.isdir(target):
        sys.exit('\n"{}" does not exist or is not a directory.'.format(target))

    manifest = os.path.join(target, '.acorn')
    do_clean(target, manifest)
    click.echo('completing clean...\t[SUCCESS]')

def do_clean(target, manifest):
    try:
        with open(manifest) as f:
            acorn = json.load(f)
    except json.JSONDecodeError:
        sys.exit('ERROR: manifest file is invalid.')
    except FileNotFoundError:
        click.echo('[OK] no files found')
        return
    click.echo('[OK] manifest loaded')

    directories = set()
    click.echo('removing files...\t', nl=False)
    total = 0
    for filename in acorn['generated']:
        fqn = os.path.join(target, *filename.split('/'))
        directories.add(os.path.dirname(fqn))
        try:
            os.remove(fqn)
            total += 1
        except FileNotFoundError:
            pass
    click.echo('[OK] {} file{} removed'.format(total, '' if total == 1 else 's'))

    click.echo('pruning directories...\t', nl=False)
    total = 0
    for directory in directories:
        try:
            if not os.listdir(directory):
                os.rmdir(directory)
                total += 1
        except FileNotFoundError:
            pass
    click.echo('[OK] {} director{} removed'.format(total, 'y' if total == 1 else 'ies'))
    
    os.remove(manifest)

def prepare_credentials():
    filename = os.path.join(os.path.expanduser('~'), '_netrc' if WINDOWS else '.netrc')
    try:
        return filename, netrc.netrc(filename).hosts.get(ACORN, None)
    except FileNotFoundError:
        open(filename, 'w+').close()
        os.chmod(filename, 0o600)
        return filename, None

def load_session():
    session = requests.Session()

    filename = os.path.join(os.path.expanduser('~'), '_netrc' if WINDOWS else '.netrc')
    try:
        credentials = netrc.netrc(filename).hosts.get(ACORN, None)
    except FileNotFoundError:
        credentials = None

    if credentials is None or not credentials[2]:
        session.close()
        sys.exit('fetching token...\t[FAIL] not logged in.')

    try:
        session.cookies = pickle.loads(base64.b64decode(credentials[0].encode()))
    except pickle.UnpicklingError:
        session.close()
        sys.exit('fetching token...\t[FAIL] not logged in.')

    r = session.post(
        '{}/auth/refresh'.format(ACORN),
        headers={'Authorization': 'Bearer {}'.format(credentials[2])})

    if not r.ok:
        session.close()
        sys.exit('fetching token...\t[FAIL] your session has expired, please log in again.')

    session.headers['Authorization'] = 'Bearer ' + r.json()['token']

    return session

def splash(action):
    f = pyfiglet.Figlet(font='big', justify='center')
    r = f.renderText('acorn')
    click.echo('-'*80)
    click.echo(r)
    click.echo('action requested: {}'.format(action).center(80))
    click.echo('-'*80)

def configure_vscode(project, path):
    fqn = os.path.join(path, '.vscode', 'tasks.json')
    updated = json.loads(
        ENV.get_template('tasks.json.j2').render(project=project)
    )

    try:
        with open(fqn) as f:
            existing = commentjson.load(f)
    except commentjson.JSONLibraryException:
        sys.exit('[FAIL] unable to parse existing vscode tasks.')
    except FileNotFoundError:
        existing = {}
    
    if 'version' in existing and existing['version'] != updated['version']:
        sys.exit('[FAIL] expecting vscode task version {} (is {}).'.format(
            updated['version'],
            existing['version']))
    
    overwritten = {x['label'] for x in updated['tasks']}
    updated['tasks'].extend(filter(
        lambda x: x.get('label', None) not in overwritten,
        existing.get('tasks', ())))

    overwritten = {x['id'] for x in updated['inputs']}
    updated['inputs'].extend(filter(
        lambda x: x.get('id', None) not in overwritten,
        existing.get('inputs', ())))
    
    existing.update(updated)
    os.makedirs(os.path.join(path, '.vscode'), exist_ok=True)
    with open(fqn, 'w') as f:
        commentjson.dump(existing, f, indent=4)

def token_hex(nbytes: int = 16):
    return binascii.hexlify(os.urandom(nbytes)).decode('ascii')

WINDOWS = platform.system() == 'Windows'
ACORN = 'https://acorn.squirreltechnologies.nz'
ENV = Environment(
    loader=PackageLoader('pyacorn', 'templates')
)
CONFIG = '''SYSTEM_STORAGE_DSN=sqlite:///{cwd}/.database.db
SYSTEM_STORAGE_ATTACHMENTS={cwd}/.attachments
SYSTEM_AUTH_ISSUER={issuer}
SYSTEM_AUTH_SECRET={secret}
SYSTEM_NETWORK_CACHE=tcp://127.0.0.1:5555
SYSTEM_NETWORK_SUBMIT=tcp://127.0.0.1:5556
SYSTEM_NETWORK_NOTIFY=tcp://127.0.0.1:5557
SYSTEM_NETWORK_CONTROL=tcp://127.0.0.1:5558
SYSTEM_MQ_DATA={cwd}/.mq
SYSTEM_MQ_SUBSCRIBE=http://127.0.0.1:5000
'''