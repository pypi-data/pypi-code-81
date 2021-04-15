"""class for configurations
"""

import json
import os
import sys
import shutil
from getpass import getpass
import importlib
import inspect
import multiprocessing as mp
from collections import defaultdict
import pymysql
import datajoint as dj
from datajoint.settings import default
from datajoint.utils import to_camel_case
from sshtunnel import SSHTunnelForwarder
from werkzeug.utils import secure_filename

from loris.database.attributes import custom_attributes_dict
from loris.utils import is_manuallookup
from loris.errors import LorisError


# defaults for application
defaults = {
    "textarea_startlength": 512,
    # UPLOAD EXTENSIONS
    "extensions": ['csv', 'npy', 'json', 'pkl', 'npz'],
    "attach_extensions": (
        ['csv', 'npy', 'json', 'pkl', 'npz'] + [
            'tiff', 'png', 'jpeg', 'mpg', 'hdf', 'hdf5', 'tar', 'zip',
            'txt', 'gif', 'svg', 'tif', 'bmp', 'doc', 'docx', 'rtf',
            'odf', 'ods', 'gnumeric', 'abw', 'xls', 'xlsx', 'ini',
            'plist', 'xml', 'yaml', 'yml', 'py', 'js', 'php', 'rb', 'sh',
            'tgz', 'txz', 'gz', 'bz2', 'jpe', 'jpg', 'pdf',
            'irradcal', 'cal'  # calibration files
        ]
    ),
    "additional_extensions": [],  # TODO
    # foreign key select field limit
    "fk_dropdown_limit": 200,
    "user_schema": "experimenters",
    "user_table": "Experimenter",
    "user_name": "experimenter",
    "group_schema": "experimenters",
    "group_table": "ExperimentalProject",
    "group_name": "experimental_project",
    "assignedgroup_schema": "experimenters",
    "assignedgroup_table": "AssignedExperimentalProject",
    "max_cpu": None,
    "init_database": True,
    "include_fly": False,
    "import_schema_module": {},  # schema_name : file_location
    "tables_skip_permission": ['`subjects`.`fly_stock`'],
    "filestores": {
        "attachstore": None,
        "datastore": None
    },
    "database.host": None,
    "database.port": None,
    "database.user": None,
    "database.password": None,
    "connection.charset": "utf8",
    "enable_python_native_blobs": True,
    "enable_python_pickle_blobs": True,
    "enable_automakers": True,
    "secret_key": "myprecious",
    "tmp_folder": "~/tmp",
    "skip_schemas": ["mysql", "sys", "performance_schema", "tutorial"],
    "user_schema": "experimenters",
    "user_table": "Experimenter",
    "user_name": "experimenter",
    "user_active": "active",
    "group_schema": "experimenters",
    "group_table": "ExperimentalProject",
    "group_name": "experimental_project",
    "assignedgroup_schema": "experimenters",
    "assignedgroup_table": "AssignedExperimentalProject",
    "standard_password": "fruitfly",
    "administrator_info": {
        "experimenter": "administrator",
        "first_name": "FIRSTNAME",
        "last_name": "LASTNAME",
        "email": "administrator@mail.com",
        "phone": "000-000-0000",
        "date_joined": "2020-01-01",
        "active": True
    },
    "administrators": ["administrator"],
    "wiki_folder": "~/loris/wiki",
    "autoscript_folder": "~/loris/autoscripts",
    "external_wiki": "#",
    "ssh_address": None,
    "ssh_username": "administrator",
    "ssh_pkey": "~/.ssh/id_rsa",
    "slack": [],
    "sql_privileges": {},
    # tables skipped to check for permission
}
AUTOSCRIPT_CONFIG = 'config.json'
USER_FILENAME = '._loris_config.json'
USER_CONFIG = os.path.join(os.path.expanduser('~'), USER_FILENAME)
GLOBAL_CONFIG = os.path.join(os.path.dirname(__file__), 'global_config.json')
EXPANDUSER_FIELDS = (
    'tmp_folder',
    'wiki_folder',
    'autoscript_folder',
    'ssh_pkey'
)


class Config(dict):

    _slack_tables = None

    @classmethod
    def load(cls, config_file):
        """load configuration class and perform necessary checks
        """

        if config_file is None:
            config_file = USER_CONFIG

            if not os.path.exists(config_file):
                config_file = 'loris_config.json'

                if not os.path.exists(config_file):
                    root_dir = os.path.dirname(os.path.dirname(__file__))
                    config_file = os.path.join(root_dir, 'config.json')

        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
            with open(USER_CONFIG, 'w') as f:
                json.dump(config, f)
        elif os.path.exists(GLOBAL_CONFIG):
            with open(GLOBAL_CONFIG, 'r') as f:
                config = json.load(f)
        else:
            config = {}

        config = {**defaults, **config}
        config = cls(config)
        config['custom_attributes'] = custom_attributes_dict
        config['_empty'] = []  # list of files in tmp to delete on refresh
        config['_autopopulate'] = {}  # dictionary of subprocesses
        # delete permissions for datajoint
        config['delete_permission'] = config.datajoint_delete_permission
        config.perform_checks()
        config.datajoint_configuration()

        return config

    def datajoint_delete_permission(self, table):
        return self.user_has_permission(table, self['database.user'])

    def user_has_permission(self, table, user, skip_tables=None):
        """test if user is allowed to delete an entry or perform another action
        on a datajoint.Table
        """

        if user is None:
            user = self['connection'].get_user().split('@')[0]

        if user in self['administrators']:
            return True

        if table.database in self.groups_of_user(user):
            return True

        if skip_tables is None:
            skip_tables = self['tables_skip_permission']
            # skip_tables = []

        # always add table name
        skip_tables.append(table.full_table_name)

        if not table.connection.dependencies:
            table.connection.dependencies.load()

        ancestors = table.ancestors()

        if self.user_table.full_table_name in ancestors:
            if self['user_name'] in table.heading:
                user_only = table & {self['user_name']: user}
                return len(user_only) == len(table)
            else:
                for parent_name, parent_info in table.parents(foreign_key_info=True):
                    if parent_name in skip_tables:
                        continue

                    # get parent table
                    parent_table = self.get_table(parent_name)

                    # project only necessary keys
                    to_rename = {
                        ele: key
                        for key, ele in parent_info['attr_map'].items()
                    }
                    restricted_table = parent_table & table.proj(**to_rename)

                    if not self.user_has_permission(
                        restricted_table, user, skip_tables
                    ):
                        return False

        # checks if children have a parent table that is dependent on user table
        for child_name, child_info in table.children(foreign_key_info=True):
            if child_name in skip_tables:
                continue

            # get child table
            child_table = self.get_table(child_name)

            # restrict only with necessary keys
            restricted_table = child_table & table.proj(**child_info['attr_map'])

            if not self.user_has_permission(
                restricted_table, user, skip_tables
            ):
                return False

        return True

    @property
    def slacks(self):
        return self.get('slack', [])

    @property
    def slack_tables(self):
        if self._slack_tables is None:
            slack_tables = {}
            for slack in self.slacks:
                if slack.get('token', None) is not None:
                    slack_tables[slack['table']] = slack

            self._slack_tables = slack_tables

        return self._slack_tables

    def connect_ssh(self):
        """ssh tunneling

        see: https://sshtunnel.readthedocs.io/en/latest/
        """

        if self.get('server', None) is not None:
            return self['server']

        elif self.get('ssh_address', None) is not None:
            # inti kwargs for init
            remote_bind_address = (
                self['database.host'], self['database.port']
            )
            kwargs = {
                'remote_bind_address': remote_bind_address,
                'local_bind_address': remote_bind_address
            }

            # get signature
            signature = inspect.signature(SSHTunnelForwarder)

            for key, param in signature.parameters.items():
                if param.name in self:
                    kwargs[param.name] = self[param.name]

            kwargs.pop('ssh_address', None)
            print('parameters for ssh tunneling:')
            print(kwargs)

            address = self['ssh_address'].split(':')
            address[1] = int(address[1])
            address = tuple(address)
            print(address)

            # mute exceptions
            kwargs['mute_exceptions'] = True
            kwargs['raise_exception_if_any_forwarder_have_a_problem'] = False

            # initialize server
            server = SSHTunnelForwarder(
                address, **kwargs
            )
            self['server'] = server

            # start server
            server.start()

            return self['server']

    def disconnect_ssh(self):
        """ssh tunneling
        """

        if self.get('server', None) is not None:
            self['server'].stop()
            self['server'] = None

    def close(self):
        self['connection'].close()
        self.pop('connection', None)
        self.disconnect_ssh()

    def __getitem__(self, k):

        try:
            return super().__getitem__(k)
        except KeyError as e:
            if k == 'tables':
                self.refresh_tables()
                return self[k]
            elif k == 'schemata':
                self.refresh_schema()
                return self[k]
            elif k == 'dynamicforms':
                self[k] = {}
                return self[k]
            elif k == 'automaker_tables':
                self.refresh_automaker_tables()
                return self[k]
            elif k == 'settings_tables':
                self.refresh_settings_tables()
                return self[k]
            elif k == 'connection':
                return self.conn(reset=True)
            elif k == 'server':
                return self.connect_ssh()

            raise e

    def conn(self, *args, **kwargs):
        """connect to database with hostname, username, and password.
        """
        newargs = dict(zip(['host', 'user', 'password'], args))
        newargs.update(kwargs)
        already_connected = 'connection' in self
        # self.datajoint_configuration()
        self.connect_ssh()
        reconfigure_dj = False
        # database host
        if self['database.host'] is None and 'host' not in newargs and not already_connected:
            host = input(
                "What is the host address for your MySQL "
                "instance (defaults to `127.0.0.1`)? "
            )
            if not host:
                host = '127.0.0.1'
            self['database.host'] = host
            reconfigure_dj = True
        # database port
        if self['database.port'] is None and 'port' not in newargs and not already_connected:
            port = input(
                "What is the port for your MySQL "
                "instance (defaults to `3306`)? "
            )
            if not port:
                port = 3306
            else:
                port = int(port)
            self['database.port'] = port
            reconfigure_dj = True
        if self['database.user'] is None and 'user' not in newargs and not already_connected:
            user = input("Please enter your Loris/MySQL username: ")
            self['database.user'] = user
            reconfigure_dj = True
        if self['database.password'] is None and 'password' not in newargs and not already_connected:
            pw = getpass(prompt="Please enter Loris/MySQL password: ")
            self['database.password'] = pw
            reconfigure_dj = True

        if reconfigure_dj:
            self.datajoint_configuration()

        if self['database.host'] == 'mysql' and 'host' not in newargs:
            try:
                self['connection'] = dj.conn(**newargs)
            except pymysql.OperationalError:
                newargs.pop('host')
                self['connection'] = dj.conn('127.0.0.1', **newargs)
        else:
            self['connection'] = dj.conn(**newargs)

        # update backup context with schemata
        if newargs.get('refresh', False):
            self.refresh_schema()
        dj.config['backup_context'].update(self['schemata'])
        return self['connection']

    def datajoint_configuration(self):
        # --- managing external file stores for database --- #
        if 'stores' not in dj.config:
            dj.config['stores'] = {}

        for filestore_name, filestore in self['filestores'].items():
            if filestore is None:
                filestore = input(
                    f"What is the directory for your `{filestore_name}` "
                    f"(defaults to `~/loris/{filestore_name}`)? "
                )
                if not filestore:
                    filestore = f"~/loris/{filestore_name}"
                self['filestores'][filestore_name] = filestore
            filestore = os.path.expanduser(filestore)
            if not os.path.exists(filestore):
                os.makedirs(filestore)

            dj.config['stores'].update({
                filestore_name: {
                    'protocol': 'file',
                    'location': filestore
                }
            })

        # set datajoint variable in datajoint config
        for key, ele in default.items():
            if key in self:
                dj.config[key] = self[key]
            else:
                self[key] = ele

        dj.config['backup_context'] = custom_attributes_dict

    def perform_checks(self):
        """perform various checks (create directories if they don't exist)
        """

        for path in EXPANDUSER_FIELDS:
            if path in self:
                self[path] = os.path.expanduser(self[path])

        if sys.platform in ['win32', 'cygwin']:
            # enforce if on Windows
            self['tmp_folder'] = '/tmp'
        if not os.path.exists(self['tmp_folder']):
            os.makedirs(self['tmp_folder'])

        self['autoscript_folder'] = os.path.realpath(
            self['autoscript_folder'])
        if not os.path.exists(self['autoscript_folder']):
            os.makedirs(self['autoscript_folder'])

        if self['max_cpu'] is None:
            self['max_cpu'] = mp.cpu_count()

    def refresh_schema(self):
        """refresh container of schemas
        """
        schemata = {}

        # direct loading if possible
        # TODO (also in app init)
        if self['init_database']:
            from loris.schema import (
                experimenters, core
            )

            schemata['experimenters'] = experimenters
            schemata['core'] = core

            if self['include_fly']:
                from loris.schema import anatomy, subjects
                schemata['anatomy'] = anatomy  # move out
                schemata['subjects'] = subjects

        for schema, module_path in self["import_schema_module"]:
            # TODO test
            spec = importlib.util.spec_from_file_location(schema, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            schemata[schema] = module

        for schema in dj.list_schemas():
            if schema in self["skip_schemas"]:
                continue
            if schema in schemata:
                continue
            # TODO error messages
            schemata[schema] = dj.VirtualModule(
                schema, schema, connection=self['connection'],
                add_objects=custom_attributes_dict,
                create_tables=True
            )
            # make sure jobs table has been created
            schemata[schema].schema.jobs

        self['schemata'] = schemata

    def get_table_from_classname(self, class_name):
        """get table from schemata using table class name format
        """

        table_info = class_name.split('.')
        schema, table_classes = table_info[0], table_info[1:]

        schema_module = self['schemata'].get(schema, None)

        if schema_module is None:
            raise LorisError(
                f'schema {schema} not in database; refresh database'
            )

        table = schema_module

        for table_ in table_classes:

            try:
                table = getattr(table, table_)
            except AttributeError:
                raise LorisError(
                    f'table {table_} not in schema {schema}; '
                    'refresh database'
                )

        return table

    def get_table(self, full_table_name):
        """get table from schemata using full_table_name
        """

        schema, table_name = full_table_name.replace('`', '').split('.')

        schema_module = self['schemata'].get(schema, None)

        if schema_module is None:
            raise LorisError(
                f'schema {schema} not in database; refresh database'
            )

        table_name = table_name.strip('_#')
        table_name_list = table_name.split('__')
        if len(table_name_list) == 1:
            table_name = to_camel_case(table_name)
            try:
                return getattr(schema_module, table_name)
            except AttributeError:
                raise LorisError(
                    f'table {table_name} not in schema {schema}; '
                    'refresh database'
                )
        else:
            assert len(table_name_list) == 2, \
                f'invalid table name {table_name}.'
            table_name = to_camel_case(table_name_list[0])
            part_table_name = to_camel_case(table_name_list[1])
            try:
                return getattr(
                    getattr(schema_module, table_name),
                    part_table_name
                )
            except AttributeError:
                raise LorisError(
                    f'table {table_name} not in schema {schema} '
                    f'or part table {part_table_name} not in table {table_name}'
                    '; refresh database'
                )

    def refresh_tables(self):
        """refresh container of tables
        """

        tables = {}

        for schema, module in self['schemata'].items():
            # skip mysql schema etc
            if schema in self["skip_schemas"]:
                continue
            for key, ele in module.__dict__.items():
                if key.split('.')[0] in self['schemata']:
                    continue

                if inspect.isclass(ele) and issubclass(ele, dj.user_tables.UserTable):
                    if is_manuallookup(ele) or issubclass(ele, dj.Settingstable):
                        continue
                    tables[f'{schema}.{key}'] = ele

                    # get part tables
                    for part_name, part_table in ele.__dict__.items():
                        if inspect.isclass(part_table):
                            if issubclass(part_table, dj.Part):
                                tables[f'{schema}.{key}.{part_name}'] = \
                                    part_table

        self['tables'] = tables

        return tables

    @property
    def user_table(self):
        """return the user table
        """

        return getattr(
            self['schemata'][self['user_schema']],
            self['user_table'])

    @property
    def users(self):
        """get a list of all users
        """
        users = list(
            self.user_table.proj(self['user_name']).fetch()[self['user_name']]
        )

        if not users:
            self.create_administrator()

        return users

    def create_administrator(self):
        # insert administrator if not users exist and create
        self.user_table.insert1(self['administrator_info'])

        # use standard password
        password = self['standard_password']
        # establish connection
        conn = self['connection']
        connection = '%'
        username = self['administrator_info'][self['user_name']]

        # for safety flush all privileges
        conn.query("FLUSH PRIVILEGES;")

        conn.query(
            "DROP USER IF EXISTS %s@%s;",
            (username, connection)
        )
        conn.query(
            "CREATE USER %s@%s IDENTIFIED BY %s;",
            (username, connection, password)
        )

        # create user-specific schema
        schema = dj.Schema(username)

        privileges = {
            '*.*': "ALL PRIVILEGES",
        }

        for dbtable, privilege in privileges.items():
            privilege = (f"GRANT {privilege} ON {dbtable} to %s@%s;")
            conn.query(privilege, (username, connection))

        conn.query("FLUSH PRIVILEGES;")

        return schema

    @property
    def user_tables(self):
        """return a list of user tables
        """
        return list(set(self.users) & set(self['schemata']))

    @property
    def group_table(self):
        """return the group table
        """

        return getattr(
            self['schemata'][self['group_schema']],
            self['group_table'])

    @property
    def groups(self):
        """get a list of all groups
        """
        groups = list(
            self.group_table.proj(
                self['group_name']
            ).fetch()[self['group_name']]
        )

        return groups

    @property
    def group_tables(self):
        """return a list of group tables
        """
        return list(set(self.groups) & set(self['schemata']))

    def create_group_schemas(self):
        """create all missing schemas
        """

        for group in self.groups:
            dj.Schema(group, connection=self['connection'])

    @property
    def assigned_table(self):
        """assigned table (matching groups and users)
        """

        return getattr(
            self['schemata'][self['assignedgroup_schema']],
            self['assignedgroup_table'])

    def groups_of_user(self, user):
        """groups user belongs to (includes user name)
        """

        groups = [user]

        table = self.assigned_table & {
            self['user_name'] : user
        }
        groups.extend(
            list(table.proj(self['group_name']).fetch()[self['group_name']])
        )

        return groups

    def schemas_of_user(self, user):
        """schemas user belongs to (should be the same as groups_of_user except
        when administrator), if each group has an associated schema.
        """

        if user in self['administrators']:
            return list(self['schemata'])

        groups = self.groups_of_user(user)
        return list(set(groups) & set(self['schemata']))

    def user_in_group(self, user, group):
        """is user in group
        """

        table = self.assigned_table & {
            self['user_name'] : user,
            self['group_name'] : group
        }

        if len(table) == 1:
            return True
        elif len(table) == 0:
            return False
        else:
            raise LorisError(
                "assined user group table should only have "
                "singular entries for given user and group."
            )

    def refresh_permissions(self):
        """refresh permissions of users
        """

        try:
            for user in self.users:
                for schema in self.schemas_of_user(user):
                    conn = self['connection']
                    conn.query("FLUSH PRIVILEGES;")
                    conn.query(
                        f"GRANT ALL PRIVILEGES ON {schema}.* to %s@%s;",
                        (user, '%')
                    )
                    conn.query("FLUSH PRIVILEGES;")
        except Exception as e:
            print(f"Did not refresh permissions! Due to \n {e}")

    def refresh_settings_tables(self):
        """refresh container of settings table
        """

        tables = {}

        for table_name, table in self['tables'].items():
            if issubclass(table, dj.Settingstable):
                tables[table_name] = table

        self['settings_tables'] = tables

        return tables

    def refresh_automaker_tables(self):
        """refresh container of settings table
        """

        tables = {}

        for table_name, table in self['tables'].items():
            if issubclass(table, (dj.AutoImported, dj.AutoComputed)):
                tables[table_name] = table

        self['automaker_tables'] = tables

        return tables

    def tables_to_list(self):
        """convert tables container to list for app header
        """

        tables = self['tables']
        manualtables_dict = defaultdict(list)
        autotables_list = []

        for table_name, table in tables.items():
            if issubclass(table, dj.Manual):
                auto_class = False
                # ignore ManualLookup subclasses
                if (
                    is_manuallookup(table)
                    or (table.full_table_name
                        == self.user_table.full_table_name)
                    or (table.full_table_name
                        == self.group_table.full_table_name)
                    or (table.full_table_name
                        == self.assigned_table.full_table_name)
                ):
                    continue
            elif issubclass(table, (dj.AutoImported, dj.AutoComputed)):
                auto_class = True
            else:
                continue

            table_list = [table_name] + table_name.split('.') + [None]

            if auto_class:
                autotables_list.append(table_list)
            else:
                manualtables_dict[table_list[1]].append(table_list[2])

        return manualtables_dict, autotables_list

    def refresh_dependencies(self):
        """refresh dependencies of database connection
        """

        self['connection'].dependencies.load()

    def empty_tmp_folder(self):
        """empty temporary folder
        """

        for filename in os.listdir(self['tmp_folder']):
            if not any([filename.startswith(ele) for ele in self['_empty']]):
                continue
            file_path = os.path.join(self['tmp_folder'], filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

        self['_empty'] = []

    def refresh(self):
        """refresh all containers and empty temporary folder
        """

        self.pop('dynamicforms', None)
        self.pop('autoscriptforms', None)
        self.empty_tmp_folder()
        self.refresh_dependencies()
        self.refresh_schema()
        self.refresh_tables()
        self.refresh_settings_tables()
        self.refresh_automaker_tables()
        self.refresh_permissions()

    def get_dynamicform(
        self, table_name, table_class, dynamic_class, **kwargs
    ):
        """get the dynamic form and wtf form for application
        """

        name = dynamic_class.__name__

        if name not in self['dynamicforms']:
            self['dynamicforms'][name] = {}

        if table_name not in self['dynamicforms'][name]:
            dynamicform = dynamic_class(table_class)
            form = dynamicform.formclass(**kwargs)
            self['dynamicforms'][name][table_name] = dynamicform
        else:
            # update foreign keys
            dynamicform = self['dynamicforms'][name][table_name]
            form = dynamicform.formclass(**kwargs)
            dynamicform.update_fields(form)

        return dynamicform, form

    def get_autoscriptforms(
        self, autoscript_filepath, table_name, form_creator, **kwargs
    ):
        """get autoscript form and process_dict and buttons params
        """
        foldername = os.path.basename(autoscript_filepath)
        filepath = os.path.join(
            autoscript_filepath, AUTOSCRIPT_CONFIG
        )

        with open(filepath, 'r') as f:
            try:
                config = json.load(f)
            except Exception as e:
                raise LorisError(
                    f"Json config file for autoscript"
                    f" '{foldername}' badly "
                    f"formatted: {e}"
                )

        if 'buttons' not in config:
            raise LorisError(
                "In configuration file of autoscript "
                f"{foldername}, no 'button' key "
                "was provided."
            )

        buttons = config['buttons']
        config_forms = config.get('forms', {})

        if not isinstance(buttons, dict):
            raise LorisError(
                f'In configuration file of autoscript '
                f'"{foldername}", '
                '"scripts" keyword is incorrectly '
                'formatted.'
            )

        for key, button in buttons.items():
            base_message = (
                f'In configuration file of autoscript '
                f'"{foldername}", '
                '"buttons" keyword is incorrectly '
                f'formatted for button "{key}":'
            )
            message = (
                f'{base_message} must be dictionary with '
                '"script" key and "validate", "insert", "configattr", '
                '"outputfile", and "outputattr" optionally defined.'
            )
            if not isinstance(button, dict):
                raise LorisError(message)
            elif not all([
                isinstance(button.get('script', None), str),
                isinstance(button.get('validate', []), list),
                isinstance(button.get('insert', False), bool),
                isinstance(button.get('configattr', ''), str),
                isinstance(button.get('outputfile', ''), (str, list)),
                isinstance(button.get('outputattr', ''), (str, list)),
            ]):
                raise LorisError(message)

            button['script'] = secure_filename(button['script'])
            if not os.path.exists(
                os.path.join(autoscript_filepath, button['script'])
            ):
                raise LorisError(
                    f'{base_message} script "{button["script"]}" '
                    'does not exist in autoscript folder.'
                )

            if (
                'outputfile' in button
                and isinstance(button['outputfile'], str)
            ):
                if not isinstance(button['outputattr'], str):
                    raise LorisError(message)
                # put into list format
                button['outputfile'] = [secure_filename(button['outputfile'])]
                button['outputattr'] = [button['outputattr']]
            elif 'outputfile' in button:
                if not (
                    isinstance(button['outputattr'], list)
                    and len(button['outputfile']) == len(button['outputattr'])
                ):
                    raise LorisError(message)

                button['outputfile'] = [
                    secure_filename(ifilepath)
                    for ifilepath in button['outputfile']
                ]

        if not isinstance(config_forms, dict):
            raise LorisError(
                f'In configuration file of autoscript '
                f'"{os.path.basename(autoscript_filepath)}", '
                '"forms" keyword is incorrectly '
                'formatted.'
            )

        forms = {}
        post_process_dict = {}
        for key, value in config_forms.items():
            form, post_process = form_creator(
                value, autoscript_filepath, **kwargs
            )
            forms[key] = form
            post_process_dict[key] = post_process

        return forms, post_process_dict, buttons
