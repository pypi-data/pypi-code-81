import html
import json
import logging
import os
import smtplib
from datetime import datetime
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional, Tuple, TextIO, Union, Callable, Dict, Any

import requests

from moonspec import _MOONSPEC_RUNTIME_STATE
from moonspec.api import HostApi
from moonspec.api.interface.fs import PathApi
from moonspec.state import SpecCaseDefinition
from moonspec.utils import ts_now_ms, date_now_format, date_now_readable_format, md5, ObjectView, \
    time_now_readable_format

LOGGER = logging.getLogger('moonspec')


# TODO: config validation is poor

def file_path_format(path: str) -> str:
    now = datetime.now()

    options = {
        'ts': int(now.timestamp()),
        'df': now.strftime('%Y_%m_%d_%H_%M_%S_%f'),
        'dy': now.strftime('%Y_%m_%d'),
        'dh': now.strftime('%H_%M_%S'),
        'dm': now.strftime('%f'),
        'h': HostApi.name(),
        's': _MOONSPEC_RUNTIME_STATE.suite_name,
    }

    try:
        return path.format(o=ObjectView(options))
    except AttributeError as e:
        LOGGER.error('Failed to format path <%s>', path)
        raise e


class Output:
    """
    Generic output interface
    """

    def on_spec_start(self, spec: SpecCaseDefinition) -> None:
        raise NotImplementedError()

    def on_spec_success(self, spec: SpecCaseDefinition) -> None:
        raise NotImplementedError()

    def on_spec_failure(
            self,
            spec: SpecCaseDefinition,
            cause: BaseException,
            soft_failures: List[BaseException]
    ) -> None:
        raise NotImplementedError()

    def on_spec_unstable(self, spec: SpecCaseDefinition, soft_failures: List[BaseException]) -> None:
        raise NotImplementedError()

    def on_complete(self, any_failed: bool) -> None:
        raise NotImplementedError()


class ObjectOutput(Output):
    """
    Just push everything into an object, as log
    """

    def __init__(self) -> None:
        self.entries: List[dict] = []

    def on_spec_start(self, spec: SpecCaseDefinition) -> None:
        self.entries.append({'type': 'start', 'name': spec.name, 'module': spec.module, 'time': ts_now_ms()})

    def on_spec_success(self, spec: SpecCaseDefinition) -> None:
        self.entries.append({'type': 'successful', 'name': spec.name, 'module': spec.module, 'time': ts_now_ms()})

    def on_spec_failure(self, spec: SpecCaseDefinition, cause: BaseException,
                        soft_failures: List[BaseException]) -> None:
        entry: Dict[str, Any] = {
            'type': 'failed',
            'name': spec.name,
            'module': spec.module,
            'time': ts_now_ms(),
            'cause': str(cause),
            'soft': []
        }

        for soft in soft_failures:
            entry['soft'].append({'cause': str(soft)})

        self.entries.append(entry)

    def on_spec_unstable(self, spec: SpecCaseDefinition, soft_failures: List[BaseException]) -> None:
        entry: Dict[str, Any] = {
            'type': 'unstable',
            'name': spec.name,
            'module': spec.module,
            'time': ts_now_ms(),
            'soft': []
        }

        for soft in soft_failures:
            entry['soft'].append({'cause': str(soft)})

        self.entries.append(entry)

    def on_complete(self, any_failed: bool) -> None:
        self.entries.append({'type': 'run_complete', 'any_failed': any_failed, 'time': ts_now_ms()})

    def to_dict(self) -> dict:
        return {'data': self.entries}

    def to_json_str(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def write_json(self, fp: TextIO) -> None:
        json.dump(self.to_dict(), fp, indent=2)


# noinspection DuplicatedCode
class HTMLOutput(Output):
    """
    Buffered HTML output, renders on-demand, with no persistence
    """

    def __init__(self) -> None:
        self.buffer: str = ''

    def on_spec_start(self, spec: SpecCaseDefinition) -> None:
        self.buffer += '''<tr class="line started">
        <th>Started</th>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>&nbsp;</td>
        </tr>''' % (
            html.escape(spec.readable_module()),
            html.escape(spec.readable_name()),
            html.escape(time_now_readable_format())
        )

    def on_spec_success(self, spec: SpecCaseDefinition) -> None:
        self.buffer += '''<tr class="line successful">
        <th>Successful</th>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>&nbsp;</td>
        </tr>''' % (
            html.escape(spec.readable_module()),
            html.escape(spec.readable_name()),
            html.escape(time_now_readable_format())
        )

    def on_spec_failure(self, spec: SpecCaseDefinition, cause: BaseException,
                        soft_failures: List[BaseException]) -> None:
        self.buffer += '''<tr class="line fail">
        <th>Failed</th>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        </tr>''' % (
            html.escape(spec.readable_module()),
            html.escape(spec.readable_name()),
            html.escape(time_now_readable_format()),
            html.escape(str(cause))
        )

        for soft in soft_failures:
            self.buffer += '''<tr class="line unstable">
            <th>Unstable</th>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            </tr>''' % (
                html.escape(spec.readable_module()),
                html.escape(spec.readable_name()),
                html.escape(time_now_readable_format()),
                html.escape(str(soft))
            )

    def on_spec_unstable(self, spec: SpecCaseDefinition, soft_failures: List[BaseException]) -> None:
        for soft in soft_failures:
            self.buffer += '''<tr class="line unstable">
            <th>Unstable</th>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            </tr>''' % (
                html.escape(spec.readable_module()),
                html.escape(spec.readable_name()),
                html.escape(time_now_readable_format()),
                html.escape(str(soft))
            )

    def on_complete(self, any_failed: bool) -> None:
        self.buffer += '''<tr class="line complete">
        <th>Complete</th>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>%s</td>
        <td>&nbsp;</td>
        </tr>''' % html.escape(date_now_readable_format())

    def to_html(self) -> str:
        html_content = f'''<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>moonspec - {html.escape(HostApi.name())} - {html.escape(date_now_readable_format())}</title>
    <style>
        * {{margin: 0; padding: 0; }}
        body, html {{
            background: #2e3440; color: #e2e2e2; margin: 0; padding: 0; font-size: 15px;
            font-family: 'SF Pro Display', 'open sans', -apple-system, BlinkMacSystemFont, 
                'segoe ui', roboto, oxygen-sans, ubuntu, cantarell, 'helvetica neue', 'arial', sans-serif,
                'apple color emoji', 'segoe ui emoji', 'segoe ui symbol';            
        }}
        #wrapper {{ padding: 20px; display: flex; justify-content: center; }}
        #content {{ flex: 0 1 auto; }}
        #title, #date {{padding-bottom: 15px;}}
        #title h1 {{font-size: 26px;font-weight: 300; margin: 0; padding: 0; }}
        #log, #log tr, #log tr td, #log tr th {{border-collapse: collapse; border: 1px solid #4c566a;}}
        #log tr td {{ padding: 5px 10px; }}
        #log tr th {{ padding: 5px 10px; text-align: left; font-weight: normal; }}
        #log tr.started th {{ color: #b48ead; }}
        #log tr.successful th {{ color: #a3be8c; }}
        #log tr.fail th {{ color: #bf616a; }}
        #log tr.unstable th {{ color: #ebcb8b; }}
        #log tr.complete th {{ color: #81a1c1; }}
    </style>
</head>
<body>
<div id="wrapper">
    <div id="content">
        <div id="title"><h1>moonspec result for spec suite "{html.escape(_MOONSPEC_RUNTIME_STATE.suite_name)}" 
            on {html.escape(HostApi.name())}</h1></div>
        <div id="date">{html.escape(date_now_readable_format())}</div>
        <table id="log">{self.buffer}</table>
    </div>
</div>
</body>
</html>'''
        return html_content


# noinspection DuplicatedCode
class MailHTMLOutput(Output):
    """
    Buffered HTML output slightly optimized for email alerting, renders on-demand, with no persistence
    """

    def __init__(self, when: str) -> None:
        self.buffer_success: str = ''
        self.buffer_failure: str = ''
        self.buffer_unstable: str = ''
        self.when = when

    def on_spec_start(self, spec: SpecCaseDefinition) -> None:
        pass

    def on_spec_success(self, spec: SpecCaseDefinition) -> None:
        self.buffer_success += '''<tr class="line successful">
        <th>Successful</th>
        <td>&nbsp;</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        </tr>''' % (
            html.escape(spec.readable_name()),
            html.escape(spec.readable_module()),
            html.escape(time_now_readable_format())
        )

    def on_spec_failure(self, spec: SpecCaseDefinition, cause: BaseException,
                        soft_failures: List[BaseException]) -> None:
        self.buffer_failure += '''<tr class="line fail">
        <th>Failed</th>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        </tr>''' % (
            html.escape(str(cause)),
            html.escape(spec.readable_name()),
            html.escape(spec.readable_module()),
            html.escape(time_now_readable_format())
        )

        for soft in soft_failures:
            self.buffer_failure += '''<tr class="line unstable">
            <th>Unstable</th>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            </tr>''' % (
                html.escape(str(soft)),
                html.escape(spec.readable_name()),
                html.escape(spec.readable_module()),
                html.escape(time_now_readable_format())
            )

    def on_spec_unstable(self, spec: SpecCaseDefinition, soft_failures: List[BaseException]) -> None:
        for soft in soft_failures:
            self.buffer_unstable += '''<tr class="line unstable">
            <th>Unstable</th>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            </tr>''' % (
                html.escape(str(soft)),
                html.escape(spec.readable_name()),
                html.escape(spec.readable_module()),
                html.escape(time_now_readable_format())
            )

    def on_complete(self, any_failed: bool) -> None:
        return

    def to_html(self) -> str:
        html_content = f'''<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>moonspec - {html.escape(HostApi.name())} - {html.escape(date_now_readable_format())}</title>
    <style>
        * {{margin: 0; padding: 0; }}
        body, html {{
            background-color: #2e3440 !important;
            background: #2e3440 !important; color: #e2e2e2 !important; margin: 0; padding: 0; font-size: 15px;
            font-family: 'SF Pro Display', 'open sans', -apple-system, BlinkMacSystemFont, 
                'segoe ui', roboto, oxygen-sans, ubuntu, cantarell, 'helvetica neue', 'arial', sans-serif,
                'apple color emoji', 'segoe ui emoji', 'segoe ui symbol';            
        }}
        #wrapper {{ padding: 20px; display: flex; justify-content: center; }}
        #content {{ flex: 0 1 auto; }}
        #title, #subtitle, #date {{padding-bottom: 15px;}}
        #title h1 {{font-size: 26px;font-weight: 300; margin: 0; padding: 0; }}
        #subtitle h2 {{font-size: 20px;font-weight: 300; margin: 0; padding: 0; }}
        #log {{margin-bottom: 15px;}}
        #log, #log tr, #log tr td, #log tr th {{border-collapse: collapse; border: 1px solid #4c566a !important;}}
        #log tr td {{ padding: 5px 10px; }}
        #log tr th {{ padding: 5px 10px; text-align: left; font-weight: normal; }}
        #log tr.started th {{ color: #b48ead !important; }}
        #log tr.successful th {{ color: #a3be8c !important; }}
        #log tr.fail th {{ color: #bf616a !important; }}
        #log tr.unstable th {{ color: #ebcb8b !important; }}
        #log tr.complete th {{ color: #81a1c1 !important; }}
    </style>
</head>
<body>
<div id="wrapper">
    <div id="content">
        <div id="title"><h1>moonspec result for spec suite "{html.escape(_MOONSPEC_RUNTIME_STATE.suite_name)}" 
            on {html.escape(HostApi.name())}</h1></div>
        <div id="date">{html.escape(date_now_readable_format())}</div>
        <div id="subtitle"><h2>Failed</h2></div>
        <table id="log">{self.buffer_failure or '<tr><td>None</td></tr>'}</table>
        <div id="subtitle"><h2>Unstable</h2></div>
        <table id="log">{self.buffer_unstable or '<tr><td>None</td></tr>'}</table>
        <div id="subtitle"><h2>Successful</h2></div>
        <table id="log">{self.buffer_success or '<tr><td>None</td></tr>'}</table>
    </div>
</div>
</body>
</html>'''
        return html_content


# noinspection DuplicatedCode
class TextOutput(Output):
    """
    Buffered text output, renders on-demand, with no persistence
    """

    def __init__(self) -> None:
        self.buffer: str = ''

    def on_spec_start(self, spec: SpecCaseDefinition) -> None:
        self.buffer += 'START\t%s\t%s\t%s\n' % (spec.readable_module(), spec.readable_name(), date_now_format())

    def on_spec_success(self, spec: SpecCaseDefinition) -> None:
        self.buffer += 'SUCCESSFUL\t%s\t%s\t%s\n' % (spec.readable_module(), spec.readable_name(), date_now_format())

    def on_spec_failure(self, spec: SpecCaseDefinition, cause: BaseException,
                        soft_failures: List[BaseException]) -> None:
        self.buffer += 'FAILED\t%s\t%s\t%s\t%s\n' % (
            spec.readable_module(),
            spec.readable_name(),
            date_now_format(),
            cause
        )
        for soft in soft_failures:
            self.buffer += 'SOFTFAIL\t%s\t%s\t%s\t%s\n' % (
                spec.readable_module(),
                spec.readable_name(),
                date_now_format(),
                soft
            )

    def on_spec_unstable(self, spec: SpecCaseDefinition, soft_failures: List[BaseException]) -> None:
        self.buffer += 'UNSTABLE\t%s\t%s\t%s\n' % (
            spec.readable_module(),
            spec.readable_name(),
            date_now_format()
        )
        for soft in soft_failures:
            self.buffer += 'SOFTFAIL\t%s\t%s\t%s\t%s\n' % (
                spec.readable_module(),
                spec.readable_name(),
                date_now_format(),
                soft
            )

    def on_complete(self, any_failed: bool) -> None:
        self.buffer += 'RUN_COMPLETE\t%s\t%s\n' % (
            date_now_format(),
            'true' if any_failed else 'false'
        )

    def to_str(self) -> str:
        return '%s\t%s\n%s' % (
            HostApi.name(),
            date_now_format(),
            self.buffer
        )

    def __str__(self) -> str:
        return self.to_str()


# noinspection DuplicatedCode
class SMTPOutput(Output):
    """
    Outputs to SMTP on completion, both plaintext and HTML
    """

    def __init__(self, options: dict):
        self.has_unstable = False
        self.text = TextOutput()

        if 'when' not in options:
            options['when'] = 'failed'
        elif not isinstance(options['when'], str) or options['when'] not in ['always', 'failed', 'successful']:
            raise RuntimeError('Failed to configure STMP output - <when> field should be either <always>, <failed>'
                               'or <successful>')

        self.html = MailHTMLOutput(options['when'])

        if 'from' not in options:
            options['from'] = HostApi.username() + '@' + HostApi.name()
        elif not isinstance(options['from'], str):
            raise RuntimeError('Failed to configure SMTP output - missing <from> string field')

        if 'to' not in options or not isinstance(options['to'], list):
            raise RuntimeError('Failed to configure SMTP output - missing <to> array field')

        if 'host' not in options or not isinstance(options['host'], str):
            raise RuntimeError('Failed to configure SMTP output - missing <host> string field')

        if 'port' not in options or not isinstance(options['port'], int):
            raise RuntimeError('Failed to configure SMTP output - missing <port> int field')

        if 'mode' not in options or not isinstance(options['mode'], str):
            raise RuntimeError('Failed to configure SMTP output - missing <mode> string field')

        self.when: str = options['when']
        self.sender: str = options['from']
        self.to: List[str] = options['to']

        self.client: Optional[Callable[[], Union[smtplib.SMTP, smtplib.SMTP_SSL]]] = None
        self.starttls: bool = False

        if 'plain' == options['mode']:
            self.client = lambda: smtplib.SMTP(
                host=options['host'],
                port=options['port']
            )
        elif 'ssl' == options['mode']:
            self.client = lambda: smtplib.SMTP_SSL(
                host=options['host'],
                port=options['port']
            )
        elif 'starttls' == options['mode']:
            self.client = lambda: smtplib.SMTP(
                host=options['host'],
                port=options['port']
            )
            self.starttls = True
        else:
            raise RuntimeError('Failed to configure SMTP client, expected mode plain, ssl, or starttls')

        username: Optional[str] = None
        password: Optional[str] = None

        if 'username' in options:
            username = options['username']
        if 'password' in options:
            password = options['password']

        self.auth: Optional[Tuple[Optional[str], Optional[str]]] = None

        if username is not None or password is not None:
            self.auth = (username, password)

    def on_spec_start(self, spec: SpecCaseDefinition) -> None:
        self.html.on_spec_start(spec)
        self.text.on_spec_start(spec)

    def on_spec_success(self, spec: SpecCaseDefinition) -> None:
        self.html.on_spec_success(spec)
        self.text.on_spec_success(spec)

    def on_spec_failure(self, spec: SpecCaseDefinition, cause: BaseException,
                        soft_failures: List[BaseException]) -> None:
        self.html.on_spec_failure(spec, cause, soft_failures)
        self.text.on_spec_failure(spec, cause, soft_failures)

    def on_spec_unstable(self, spec: SpecCaseDefinition, soft_failures: List[BaseException]) -> None:
        self.has_unstable = True
        self.html.on_spec_unstable(spec, soft_failures)
        self.text.on_spec_unstable(spec, soft_failures)

    def on_complete(self, any_failed: bool) -> None:
        if 'failed' == self.when and any_failed is False:
            return

        if 'successful' == self.when and any_failed is True:
            return

        self.html.on_complete(any_failed)
        self.text.on_complete(any_failed)

        message = MIMEMultipart('alternative')
        message['Subject'] = Header('%smoonspec spec %s on %s, suite %s, at %s' % (
            '[FAILED] ' if any_failed else ('[UNSTABLE] ' if self.has_unstable else '[OK] '),
            'failed ' if any_failed else ('unstable ' if self.has_unstable else 'success '),
            HostApi.name(),
            _MOONSPEC_RUNTIME_STATE.suite_name,
            date_now_readable_format()
        ), 'utf-8')
        message['From'] = self.sender

        message.attach(MIMEText(self.text.to_str(), 'plain', _charset='utf-8'))
        message.attach(MIMEText(self.html.to_html(), 'html', _charset='utf-8'))

        try:
            if self.client is None:
                raise RuntimeError()

            server = self.client()

            if self.auth is not None:
                server.login(self.auth[0] or '', self.auth[1] or '')

            server.sendmail(
                from_addr=self.sender,
                to_addrs=self.to,
                msg=message.as_string()
            )

            server.quit()
        except BaseException as e:
            LOGGER.error('Failed to send SMTP mail', exc_info=e)


# noinspection DuplicatedCode
class HTMLFileOutput(Output):
    """
    Outputs to HTML file continuously overwriting the contents on each event
    """

    def __init__(self, options: dict):
        if 'file' not in options:
            raise RuntimeError('HTML output configuration error - missing file target')

        self.file: str = os.path.abspath(file_path_format(options['file']))
        self.parent: HTMLOutput = HTMLOutput()

    def on_spec_start(self, spec: SpecCaseDefinition) -> None:
        self.parent.on_spec_start(spec)
        self.dump()

    def on_spec_success(self, spec: SpecCaseDefinition) -> None:
        self.parent.on_spec_success(spec)
        self.dump()

    def on_spec_failure(self, spec: SpecCaseDefinition, cause: BaseException,
                        soft_failures: List[BaseException]) -> None:
        self.parent.on_spec_failure(spec, cause, soft_failures)
        self.dump()

    def on_spec_unstable(self, spec: SpecCaseDefinition, soft_failures: List[BaseException]) -> None:
        self.parent.on_spec_unstable(spec, soft_failures)
        self.dump()

    def on_complete(self, any_failed: bool) -> None:
        self.parent.on_complete(any_failed)
        self.dump()

    def dump(self) -> None:
        if PathApi.is_file(self.file) and not PathApi.can_write(self.file):
            raise RuntimeError('Can not write to file <%s>' % self.file)

        base = os.path.dirname(self.file)

        if not PathApi.is_dir(base) or not PathApi.can_write(base):
            raise RuntimeError('Path <%s> must be a writable directory' % base)

        try:
            with open(self.file, 'w+') as f:
                f.write(self.parent.to_html())
        except BaseException as e:
            LOGGER.error('Failed to write HTML', exc_info=e)


# noinspection DuplicatedCode
class LogFileOutput(Output):
    """
    Outputs to log file, continuously appending on each event
    """

    def __init__(self, options: dict):
        if 'file' not in options or not isinstance(options['file'], str):
            raise RuntimeError('Failed to configure log file output: missing <file> string field')

        fname = os.path.abspath(file_path_format(options['file']))
        self.logger: logging.Logger = logging.getLogger(md5(fname))
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler(fname)
        handler.setFormatter(logging.Formatter('%(message)s'))

        self.logger.addHandler(handler)

    def on_spec_start(self, spec: SpecCaseDefinition) -> None:
        self.logger.info('START %s %s %s' % (spec.readable_module(), spec.readable_name(), date_now_format()))

    def on_spec_success(self, spec: SpecCaseDefinition) -> None:
        self.logger.info('SUCCESSFUL %s %s %s' % (spec.readable_module(), spec.readable_name(), date_now_format()))

    def on_spec_failure(self, spec: SpecCaseDefinition, cause: BaseException,
                        soft_failures: List[BaseException]) -> None:
        self.logger.info('FAILED %s %s %s %s' % (
            spec.readable_module(),
            spec.readable_name(),
            date_now_format(),
            cause
        ))
        for soft in soft_failures:
            self.logger.info('SOFTFAIL %s %s %s %s' % (
                spec.readable_module(),
                spec.readable_name(),
                date_now_format(),
                soft
            ))

    def on_spec_unstable(self, spec: SpecCaseDefinition, soft_failures: List[BaseException]) -> None:
        self.logger.info('UNSTABLE %s %s %s' % (
            spec.readable_module(),
            spec.readable_name(),
            date_now_format()
        ))
        for soft in soft_failures:
            self.logger.info('SOFTFAIL %s %s %s %s' % (
                spec.readable_module(),
                spec.readable_name(),
                date_now_format(),
                soft
            ))

    def on_complete(self, any_failed: bool) -> None:
        self.logger.info('RUN_COMPLETE %s %s' % (
            date_now_format(),
            'true' if any_failed else 'false'
        ))


# noinspection DuplicatedCode
class ResultFileOutput(Output):
    """
    Outputs text format result to a file on completion
    """

    def __init__(self, options: dict):
        self.parent: TextOutput = TextOutput()

        if 'file' not in options or not isinstance(options['file'], str):
            raise RuntimeError('Failed to configure log file output: missing <file> string field')

        self.file: str = os.path.abspath(file_path_format(options['file']))

    def on_spec_start(self, spec: SpecCaseDefinition) -> None:
        self.parent.on_spec_start(spec)

    def on_spec_success(self, spec: SpecCaseDefinition) -> None:
        self.parent.on_spec_success(spec)

    def on_spec_failure(self, spec: SpecCaseDefinition, cause: BaseException,
                        soft_failures: List[BaseException]) -> None:
        self.parent.on_spec_failure(spec, cause, soft_failures)

    def on_spec_unstable(self, spec: SpecCaseDefinition, soft_failures: List[BaseException]) -> None:
        self.parent.on_spec_unstable(spec, soft_failures)

    def on_complete(self, any_failed: bool) -> None:
        self.parent.on_complete(any_failed)
        try:
            with open(self.file, 'w') as f:
                f.write(self.parent.to_str())
        except BaseException as e:
            LOGGER.error('Failed to write to file', exc_info=e)


# noinspection DuplicatedCode
class DataFileOutput(Output):
    """
    Outputs JSON to file on completion
    """

    def __init__(self, options: dict):
        self.parent: ObjectOutput = ObjectOutput()

        if 'file' not in options or not isinstance(options['file'], str):
            raise RuntimeError('Failed to configure data file output: missing <file> string field')

        self.file: str = os.path.abspath(file_path_format(options['file']))

    def on_spec_start(self, spec: SpecCaseDefinition) -> None:
        self.parent.on_spec_start(spec)

    def on_spec_success(self, spec: SpecCaseDefinition) -> None:
        self.parent.on_spec_success(spec)

    def on_spec_failure(self, spec: SpecCaseDefinition, cause: BaseException,
                        soft_failures: List[BaseException]) -> None:
        self.parent.on_spec_failure(spec, cause, soft_failures)

    def on_spec_unstable(self, spec: SpecCaseDefinition, soft_failures: List[BaseException]) -> None:
        self.parent.on_spec_unstable(spec, soft_failures)

    def on_complete(self, any_failed: bool) -> None:
        self.parent.on_complete(any_failed)

        try:
            with open(self.file, 'w') as f:
                self.parent.write_json(f)
        except BaseException as e:
            LOGGER.error('Failed to write output', exc_info=e)


# noinspection DuplicatedCode
class WebhookOutput(Output):
    """
    Calls a webhook with POST JSON body on completion
    """

    def __init__(self, options: dict):
        self.object_output: ObjectOutput = ObjectOutput()

        if 'when' not in options:
            options['when'] = 'failed'
        elif not isinstance(options['when'], str) or options['when'] not in ['always', 'failed', 'successful']:
            raise RuntimeError('Failed to configure webhook output - <when> field should be either <always>, <failed>'
                               'or <successful>')

        if 'url' not in options or not isinstance(options['url'], str):
            raise RuntimeError('Failed to configure webhook output - missing <url> string field')

        self.when: str = options['when']
        self.url: str = options['url']

    def on_spec_start(self, spec: SpecCaseDefinition) -> None:
        self.object_output.on_spec_start(spec)

    def on_spec_success(self, spec: SpecCaseDefinition) -> None:
        self.object_output.on_spec_success(spec)

    def on_spec_failure(self, spec: SpecCaseDefinition, cause: BaseException,
                        soft_failures: List[BaseException]) -> None:
        self.object_output.on_spec_failure(spec, cause, soft_failures)

    def on_spec_unstable(self, spec: SpecCaseDefinition, soft_failures: List[BaseException]) -> None:
        self.object_output.on_spec_unstable(spec, soft_failures)

    def on_complete(self, any_failed: bool) -> None:
        self.object_output.on_complete(any_failed)

        if 'failed' == self.when and any_failed is False:
            return

        if 'successful' == self.when and any_failed is True:
            return

        try:
            requests.post(
                url=self.url,
                json=self.object_output.to_dict()
            )
        except BaseException as e:
            LOGGER.error('Failed to send webhook', exc_info=e)


class CompositeOutput(Output):
    """
    Chained outputs
    """

    def __init__(self, instances: Optional[List[Output]] = None):
        if instances is None:
            instances = []

        self.instances: List[Output] = instances

    def on_spec_start(self, spec: SpecCaseDefinition) -> None:
        for instance in self.instances:
            instance.on_spec_start(spec)

    def on_spec_success(self, spec: SpecCaseDefinition) -> None:
        for instance in self.instances:
            instance.on_spec_success(spec)

    def on_spec_failure(
            self,
            spec: SpecCaseDefinition,
            cause: BaseException,
            soft_failures: List[BaseException]
    ) -> None:
        for instance in self.instances:
            instance.on_spec_failure(spec, cause, soft_failures)

    def on_spec_unstable(self, spec: SpecCaseDefinition, soft_failures: List[BaseException]) -> None:
        for instance in self.instances:
            instance.on_spec_unstable(spec, soft_failures)

    def on_complete(self, any_failed: bool) -> None:
        for instance in self.instances:
            instance.on_complete(any_failed)

    @staticmethod
    def from_config(output_list: List[dict]) -> 'CompositeOutput':
        outputs_by_type = {
            'html_file': HTMLFileOutput,
            'log_file': LogFileOutput,
            'data_file': DataFileOutput,
            'result_file': ResultFileOutput,
            'smtp': SMTPOutput,
            'webhook': WebhookOutput
        }
        instances = []

        for output in output_list:
            if 'type' not in output:
                LOGGER.error('Output is missing type - %s', output)
                exit(-1)

            if output['type'] not in outputs_by_type:
                LOGGER.error('Output type unknown - %s', output)
                exit(-1)

            if 'options' not in output:
                output['options'] = {}

            try:
                instances.append(outputs_by_type[output['type']](output['options']))
            except BaseException as e:
                LOGGER.error('Failed to configure output', exc_info=e)
                exit(-1)

        return CompositeOutput(instances)
