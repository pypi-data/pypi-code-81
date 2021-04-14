__version__ = '0.0.2'

from subprocess import call, list2cmdline

import yaml
import argparse
import os
import re

REGEX_ENV_WITH_DEFAULT = re.compile(r'\${(.+):-(.+)}')


def run_postgres(
        file,
        command,
        disable_tty,
        docker_compose_command,
        print_command,
        env_postgres_user,
        env_postgres_db,
        default_user,
        service,
        user,
        db):
    with open(file, 'r') as f:
        yml = yaml.safe_load(f)
        service_name = service or find_postgres_service(yml)
        environment = extract_environment(yml, service_name)

        user = user or environment.get(env_postgres_user) or default_user
        db = db or environment.get(env_postgres_db) or user

        a = [docker_compose_command]
        a.extend([] if file == 'docker-compose.yml' else ['-f', file])
        a.append('exec')
        a.extend(['-T'] if disable_tty else [])
        a.append(service_name)
        a.append('psql')
        a.append('-U')
        a.append(user)
        a.append(db)
        a.extend(['-c', command] if command else [])

        if print_command:
            print(list2cmdline(a))
        else:
            call(a)


def find_postgres_service(yml):
    for (k, v) in yml.get('services', {}).items():
        img = v.get('image')
        if img.startswith('postgres:') or img == 'postgres':
            return k
    return None


def extract_environment(yml, service_name):
    service = yml.get('services', {}).get(service_name)
    if not service:
        raise ValueError(
            'service `{}` is not defined in docker-compose file'.format(
                service_name))
    environment = service.get('environment', None)
    if environment:
        environment = \
            dict([(k, resolve_env(v)) for (k, v) in environment.items()])
    if not environment:
        env_file = service.get('env_file')
        if isinstance(env_file, list):
            environment = read_env_files(env_file)
            pass
        elif isinstance(env_file, str):
            environment = read_env_file(env_file)
        elif env_file is None:
            environment = read_env_file('.env')
        else:
            raise ValueError('env_file bad format ' + str(env_file))
    return environment


def resolve_env(value):
    m = REGEX_ENV_WITH_DEFAULT.match(value)
    if m:
        value = os.environ.get(m[1]) or m[2]
    return value


def removeprefix(s, prefix):
    if s.startswith(prefix):
        return s[len(prefix):]
    else:
        return s


def split_env_str(s):
    return s.split('=', 1)


def read_env_file(path):
    with open(path) as f:
        lines = f.read().splitlines()
        lines = [split_env_str(removeprefix(i, 'export ')) for i in lines]
        return dict(lines)


def read_env_files(paths):
    e = {}
    for path in paths:
        e.update(read_env_file(path))
    return e


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--command',
        help='run only single command (SQL or internal) and exit')
    parser.add_argument(
        '-T', default=False, action='store_true',
        help='disable pseudo-tty allocation. '
             'By default `docker-compose exec allocates a TTY.')
    parser.add_argument(
        '--docker-compose-command',
        help='path to docker-compose executable. Default `docker-compose`',
        default='docker-compose')
    parser.add_argument(
        '-p',
        '--print', dest='print_command',
        help='do not call subprocess. Print command only.',
        default=False, action='store_true')
    parser.add_argument(
        '-f', '--file',
        help='specify an alternate compose file (default: docker-compose.yml)',
        default='docker-compose.yml')
    parser.add_argument(
        '--env-user',
        help='environment variable which defines username. '
             'Default `POSTGRES_USER`',
        default='POSTGRES_USER')
    parser.add_argument(
        '--env-db',
        help='environment variable which defines dbname. '
             'Default `POSTGRES_DB`',
        default='POSTGRES_DB')
    parser.add_argument(
        '--service',
        help='specify name of service. Default behaviour is to'
             ' find service with image name starts with `postgres:`'
    )
    parser.add_argument('-U', '--username', help='database user name')
    parser.add_argument('-d', '--dbname', help='database name')
    args = parser.parse_args()
    run_postgres(
        file=args.file,
        command=args.command,
        disable_tty=args.T,
        docker_compose_command=args.docker_compose_command,
        print_command=args.print_command,
        env_postgres_user=args.env_user,
        env_postgres_db=args.env_db,
        default_user='postgres',
        service=args.service,
        user=args.username,
        db=args.dbname
    )


if __name__ == '__main__':
    main()
