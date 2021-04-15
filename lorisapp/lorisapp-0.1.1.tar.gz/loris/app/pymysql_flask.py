"""
modified from https://github.com/Viruzzz-kun/flask-pymysql/blob/master/flask_pymysql/__init__.py
"""

from flask_login import current_user

from loris import config


class MySQL(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the `app` for use with this
        :class:`~MySQL` class.
        This is called automatically if `app` is passed to
        :meth:`~MySQL.__init__`.

        :param flask.Flask app: the application to configure for use with
            this :class:`~flask_mysqldb.MySQL` class.
        """

        print('init sql')
        config.conn()
        self.app.config['schemata'] = list(config['schemata'].keys())
        self.app.config['tables'], self.app.config['autotables'] = \
            config.tables_to_list()
        config.close()
        print('closed connection')

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)

        if hasattr(app, 'before_request'):
            app.before_request(self.connect)

    def connect(self):
        print('opening')
        # TODO
        # if current_user.is_authenticated:
        #     connection = config.conn(
        #         user=current_user.user_name,
        #         password=current_user.password,
        #         reset=True
        #     )
        # else:
        connection = config.conn(
            reset=True
        )
        # not very efficient to register schema across connection
        for key, module in config['schemata'].items():
            connection.register(module.schema)
        print(connection)

    def teardown(self, exception):
        print('closing')
        config.close()
