# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from jinja2 import Environment, PackageLoader
from urllib.parse import quote

import ast
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
@click.option('--merge', is_flag=True)
def generate_project(project, path, version, branch, vscode, force_project, runtime, merge):
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
    errored = False
    for filename in acorn['editable']:
        fqn = os.path.join(target, *filename.split('/'))
        parent = os.path.dirname(fqn)
        if parent not in directories:
            directories.add(parent)
            os.makedirs(parent, exist_ok=True)

        if not os.path.exists(fqn):
            zf.extract(filename, path=target)
        elif fqn.endswith('realm.py') and merge:
            errored = merge_python_realm(zf, filename, target, fqn) or errored

    if errored:
        click.echo('[WARNING] {} roots shifted, but not all files could be merged'.format(len(acorn['editable'])))
    else:
        click.echo('[OK] {} roots shifted'.format(len(acorn['editable'])))
    
    click.echo('finalizing growth...\t', nl=False)
    for directory, files in ignored.items():
        parent = os.path.join(target, directory)
        if os.path.isdir(parent):
            with open(os.path.join(parent, '.gitignore'), 'w') as f:
                f.write('\n'.join(files))

    if vscode:
        configure_vscode(metadata['name'], target, project)

    click.echo('[SUCCESS]')

@cli.command(name='graft')
@click.argument('project')
@click.argument('path', type=click.Path())
@click.option('--version', type=VersionType())
@click.option('--branch', default="master")
@click.option('--runtime', '-r', default="python3")
@click.option('--merge', is_flag=True)
def generate_client(project, path, version, branch, runtime, merge):
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

    errored = False
    click.echo('checking roots...\t', nl=False)
    for filename in acorn['editable']:
        fqn = os.path.join(target, *filename.split('/'))
        parent = os.path.dirname(fqn)
        if parent not in directories:
            directories.add(parent)
            os.makedirs(parent, exist_ok=True)

        if not os.path.exists(fqn):
            zf.extract(filename, path=target)
        elif fqn.endswith('realm.py') and merge:
            errored = merge_python_realm(zf, filename, target, fqn) or errored

    if errored:
        click.echo('[WARNING] {} roots shifted, but not all files could be merged'.format(len(acorn['editable'])))
    else:
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
@click.option('--merge', is_flag=True)
def generate_target(project, token, path, version, branch, no_metadata, merge):
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
    errored = False
    for filename in acorn['editable']:
        fqn = os.path.join(target, *filename.split('/'))
        parent = os.path.dirname(fqn)
        if parent not in directories:
            directories.add(parent)
            os.makedirs(parent, exist_ok=True)

        if not os.path.exists(fqn):
            zf.extract(filename, path=target)
        elif fqn.endswith('realm.py') and merge:
            errored = merge_python_realm(zf, filename, target, fqn) or errored

    if errored:
        click.echo('[WARNING] {} roots shifted, but not all files could be merged'.format(len(acorn['editable'])))
    else:
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

def merge_python_realm(zf, filename, target, fqn):
    src = zf.read(filename).decode()
    with open(fqn) as f:
        dst = f.read()

    try:
        left = ast.parse(src)
        right = ast.parse(dst)
    except:
        return True

    slines = src.splitlines()
    dlines = dst.splitlines()
    tree = MergeNode()
    TreeBuildingVisitor(tree, len(slines) + 1).visit(left)
    TreeMergingVisitor(tree, slines, dlines).visit(right)

    merged = os.linesep.join(tree.merge(slines))
    with open(fqn, 'w') as f:
        f.write(merged)
    return False

def splash(action):
    f = pyfiglet.Figlet(font='big', justify='center')
    r = f.renderText('acorn')
    click.echo('-'*80)
    click.echo(r)
    click.echo('action requested: {}'.format(action).center(80))
    click.echo('-'*80)

def configure_vscode(project, path, token):
    os.makedirs(os.path.join(path, '.vscode'), exist_ok=True)

    configure_vscode_tasks(project, path, token)
    configure_vscode_launch(project, path)

    fqn = os.path.join(path, '.vscode', 'settings.json')
    updated = json.loads(
        ENV.get_template('settings.json.j2').render(project=project)
    )

    try:
        with open(fqn) as f:
            existing = commentjson.load(f)
    except commentjson.JSONLibraryException:
        sys.exit('[FAIL] unable to parse existing vscode settings.')
    except FileNotFoundError:
        existing = {}
    
    existing.update(updated)
    with open(fqn, 'w') as f:
        commentjson.dump(existing, f, indent=4)

def configure_vscode_launch(project, path):
    fqn = os.path.join(path, '.vscode', 'launch.json')
    updated = json.loads(
        ENV.get_template('launch.json.j2').render(project=project)
    )

    try:
        with open(fqn) as f:
            existing = commentjson.load(f)
    except commentjson.JSONLibraryException:
        sys.exit('[FAIL] unable to parse existing vscode launch config.')
    except FileNotFoundError:
        existing = {}
    
    if 'version' in existing and existing['version'] != updated['version']:
        sys.exit('[FAIL] expecting vscode task version {} (is {}).'.format(
            updated['version'],
            existing['version']))
    
    overwritten = {x['name'] for x in updated['configurations']}
    updated['configurations'].extend(filter(
        lambda x: x.get('name', None) not in overwritten,
        existing.get('configurations', ())))
    
    existing.update(updated)
    with open(fqn, 'w') as f:
        commentjson.dump(existing, f, indent=4)

def configure_vscode_tasks(project, path, token):
    fqn = os.path.join(path, '.vscode', 'tasks.json')
    updated = json.loads(
        ENV.get_template('tasks.json.j2').render(project=project, token=token)
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

class MergeNode:

    def __init__(self, name=None):
        self.name = name
        self.existing = []
        self.pending = []
        self.children = {}
        self.captured = {}
        self.order = []
    
    def add_child(self, name: str, lineno: int):
        self.pending.append((name, lineno))
        child = MergeNode(name)
        self.children[name] = child
        self.order.append(name)
        return child

    def add_import(self, module: str, level: int, name: str, alias: str, lineno: int):
        key = (module, level, name, alias)
        self.pending.append((key, lineno))
        self.order.append(key)

    def ack_import(self, module: str, level: int, name: str, alias: str):
        self.captured.pop((module, level, name, alias), None)

    def ack_function(self, name: str):
        self.captured.pop(name, None)
        self.children.pop(name, None)

    def merge(self, src):
        for key in filter(lambda x: x in self.captured and x not in self.children, self.order):
            (i, j) = self.captured[key]
            yield from src[i-1:j-1]

        yield from self.existing

        for key in filter(lambda x: x in self.children, self.order):
            child = self.children[key]
            if child.existing:
                yield from child.merge(src)
            else:
                (i, j) = self.captured[key]
                yield from src[i-1:j-1]

    def flush(self, term: int):
        for (key, idx) in self.pending:
            self.captured[key] = (idx, term)
            if key in self.children:
                self.children[key].flush(term)
        self.pending.clear()
    
    def __str__(self):
        return f"MergeNode<{self.name}>"


class TreeMergingVisitor(ast.NodeVisitor):

    def __init__(self, tree, src, dst):
        self.tree = tree
        self.capturing = tree
        self.idx = 0
        self.src = src
        self.dst = dst

    def visit_Import(self, node: ast.Import):
        self.inject(node.lineno)
        for name in node.names:
            self.tree.ack_import(name.name, 0, None, name.asname)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        self.inject(node.lineno)
        for name in node.names:
            self.tree.ack_import(node.module, node.level, name.name, name.asname)

    def visit_Module(self, node: ast.Module):
        for child in node.body:
            self.visit(child)
        self.capturing.existing.extend(self.dst[self.idx:len(self.dst)])
        self.idx = len(self.dst)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.tree.ack_function(node.name)
        self.inject(node.lineno)
    
    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name in self.tree.children:
            self.inject(node.lineno - 1)
            cached = self.tree
            try:
                self.tree = self.tree.children[node.name]
                self.capturing = self.tree
                for child in node.body:
                    self.visit(child)
            finally:
                self.tree = cached
    def generic_visit(self, node):
        pass

    def inject(self, lineno):
        self.capturing.existing.extend(self.dst[self.idx:lineno])
        self.capturing = self.tree
        self.idx = lineno

class TreeBuildingVisitor(ast.NodeVisitor):

    def __init__(self, tree: MergeNode, line: int):
        self.tree = tree
        self.line = line

    def visit_Module(self, node: ast.Module):
        for child in node.body:
            self.visit(child)
        self.tree.flush(self.line)

    def visit_Import(self, node: ast.Import):
        self.tree.flush(node.lineno)
        for name in node.names:
            self.tree.add_import(name.name, 0, None, name.asname, node.lineno)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        self.tree.flush(node.lineno)
        for name in node.names:
            self.tree.add_import(node.module, node.level, name.name, name.asname, node.lineno)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.tree.flush(node.lineno)
        self.capturing = self.tree.add_child(node.name, node.lineno)
    
    def visit_ClassDef(self, node: ast.ClassDef):
        self.tree.flush(node.lineno)
        cached = self.tree
        try:
            self.tree = self.tree.add_child(node.name, node.lineno)
            for child in node.body:
                self.visit(child)
        finally:
            self.tree = cached

    def generic_visit(self, node):
        pass