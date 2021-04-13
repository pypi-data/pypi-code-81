import asyncio
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import logging
import ssl
from urllib.parse import quote
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from tornado.httpclient import HTTPClientError
from tinybird.syncasync import sync_to_async


HOST = 'https://api.tinybird.co'
LOGIN_URL = 'https://ui.tinybird.co/auth/google'


class AuthException(Exception):
    pass


class AuthNoTokenException(AuthException):
    pass


class DoesNotExistException(Exception):
    pass


class CanNotBeDeletedException(Exception):
    pass


class TinyB(object):

    def __init__(self, token, host=HOST, version=None):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        self.token = token
        self.host = host
        self.version = version
        self._http_client = SimpleAsyncHTTPClient(defaults=dict(allow_nonstandard_methods=True, ssl_options=ctx))

    async def _req(self, endpoint, data=None, method='GET'):  # noqa: C901
        url = self.host + endpoint

        if self.token:
            url += ('&' if '?' in endpoint else '?') + 'token=' + self.token
        if self.version:
            url += ('&' if '?' in url else '?') + 'cli_version=' + quote(self.version)

        try:
            response = await self._http_client.fetch(url, method=method, body=data)
        except HTTPClientError as e:
            response = e.response
        except Exception as e:
            raise AuthException(f"Error on auth: {e}")

        logging.debug("== server response ==")
        logging.debug(response.body)
        logging.debug("==      end        ==")

        if response.code == 403:
            response = json.loads(response.body)
            error = response['error'] if 'error' in response else response
            if not self.token:
                raise AuthNoTokenException(f"Forbidden: {error}")
            raise AuthException(f"Forbidden: {error}")
        if response.code == 204 or response.code == 205:
            return None
        if response.code == 404:
            raise DoesNotExistException()
        if response.code == 500:
            response = json.loads(response.body)
            raise Exception(response['error'] if 'error' in response else json.dumps(response, indent=4))
        if response.code == 409:
            response = json.loads(response.body)
            raise CanNotBeDeletedException(response['error'] if 'error' in response else json.dumps(response, indent=4))
        if 'Content-Type' in response.headers and (response.headers['Content-Type'] == 'text/plain' or 'text/csv' in response.headers['Content-Type']):
            return response.body.decode()
        if response.body:
            try:
                response = json.loads(response.body)
            except json.decoder.JSONDecodeError:
                response = {
                    'error': 'Server error, cannot parse response'
                }

        if 'error' in response:
            raise Exception(response['error'])

        return response

    async def tokens(self):
        tokens = await self._req("/v0/tokens")
        return tokens['tokens']

    async def get_token_by_name(self, name):
        tokens = await self.tokens()
        for tk in tokens:
            if tk['name'] == name:
                return tk
        return None

    async def datasources(self, branch=None):
        response = await self._req("/v0/datasources")
        ds = response['datasources']

        if branch:
            ds = [x for x in ds if x['name'].startswith(branch)]
        return ds

    async def datasource_file(self, ds):
        return await self._req(f"/v0/datasources/{ds}.datasource")

    async def pipe_file(self, pipe):
        return await self._req(f"/v0/pipes/{pipe}.pipe")

    async def datasource_analyze(self, url, type_guessing=True):
        return await self._req(f"/v0/datasources?dry=true&url={url}&type_guessing={'true' if type_guessing else 'false'}", method='POST', data=b'')

    async def datasource_analyze_file(self, data, type_guessing=True):
        return await self._req(f"/v0/datasources?dry=true&type_guessing={'true' if type_guessing else 'false'}", method='POST', data=data)

    async def datasource_create(self, table_name, url, mode='create', status_callback=None, sql_condition=None):
        req_url = f"/v0/datasources?name={table_name}&url={url}&mode={mode}&debug=blocks,block_log"
        if sql_condition:
            req_url = f"{req_url}&replace_condition={quote(sql_condition, safe='')}"
        res = await self._req(req_url, method='POST', data=b'')

        if 'error' in res:
            raise Exception(res['error'])

        return await self.wait_for_job(res['id'], status_callback, backoff_multiplier=1.5, maximum_backoff_seconds=20)

    async def datasource_delete(self, datasource_name):
        return await self._req(f"/v0/datasources/{datasource_name}", method='DELETE', data=b'')

    async def datasource_append_data(self, datasource_name, f, mode='append', status_callback=None, sql_condition=None):
        url = f"{self.host}/v0/datasources?mode={mode}&name={datasource_name}&debug=blocks,block_log"
        if sql_condition:
            url = f"{url}&replace_condition={quote(sql_condition, safe='')}"
        if self.version:
            url += ('&' if '?' in url else '?') + 'cli_version=' + quote(self.version)

        m = MultipartEncoder(fields={'csv': ('csv', f, 'text/csv')})

        requests_post = sync_to_async(requests.post)

        r = await requests_post(
            url,
            data=m,
            headers={
                'Authorization': 'Bearer ' + self.token, 'Content-Type': m.content_type
            }
        )

        if r.status_code != 200:
            raise Exception(r.json())

        res = r.json()

        if status_callback:
            status_callback(res)

        return res

    async def datasource_truncate(self, datasource_name):
        return await self._req(f"/v0/datasources/{datasource_name}/truncate", method='POST', data=datasource_name.encode())

    async def pipes(self, branch=None):
        response = await self._req("/v0/pipes")
        pipes = response['pipes']
        if branch:
            pipes = [x for x in pipes if x['name'].startswith(branch)]
        return pipes

    async def pipe(self, pipe):
        return await self._req(f"/v0/pipes/{pipe}")

    async def pipe_data(self, pipe_name_or_uid, sql=None):
        if not sql:
            sql = f"SELECT * FROM {pipe_name_or_uid} LIMIT 50"
        return await self._req(f"/v0/pipes/{pipe_name_or_uid}.json?q={quote(sql, safe='')}")

    async def pipe_create(self, pipe_name, sql):
        return await self._req(f"/v0/pipes?name={pipe_name}&sql={quote(sql, safe='')}", method='POST', data=sql.encode())

    async def pipe_delete(self, pipe_name):
        return await self._req(f"/v0/pipes/{pipe_name}", method='DELETE', data=b'')

    async def pipe_append_node(self, pipe_name_or_uid, sql):
        return await self._req(f"/v0/pipes/{pipe_name_or_uid}/append", method='POST', data=sql.encode())

    async def pipe_set_endpoint(self, pipe_name_or_uid, published_node_uid):
        return await self._req(f"/v0/pipes/{pipe_name_or_uid}/endpoint", method='PUT', data=published_node_uid.encode())

    async def query(self, sql):
        return await self._req(f"/v0/sql?q={quote(sql, safe='')}")

    async def jobs(self, status=None):
        jobs = (await self._req("/v0/jobs"))['jobs']
        if status:
            status = [status] if isinstance(status, str) else status
            jobs = [j for j in jobs if j['status'] in status]
        return jobs

    async def job(self, job_id):
        return await self._req(f"/v0/jobs/{job_id}")

    async def job_cancel(self, job_id):
        return await self._req(f"/v0/jobs/{job_id}/cancel", method='POST', data=b'')

    async def workspaces(self):
        return await self._req("/v0/user/workspaces")

    async def workspace(self, workspace_id, with_token=False):
        with_token = 'true' if with_token else 'false'
        return await self._req(f"/v0/workspaces/{workspace_id}?with_token={with_token}")

    async def wait_for_job(
            self, job_id, status_callback=None, backoff_seconds=2.0,
            backoff_multiplier: float = 1, maximum_backoff_seconds=2.0):
        done = False

        while not done:
            res = await self._req("/v0/jobs/" + job_id + '?debug=blocks,block_log')
            if res['status'] == 'error':
                error_message = 'There has been an error'
                if not isinstance(res.get('error', True), bool):
                    error_message = str(res['error'])
                if 'errors' in res:
                    error_message += f": {res['errors']}"
                raise Exception(error_message)

            if res['status'] == 'cancelled':
                raise Exception('Job has been cancelled')

            done = res['status'] == 'done'

            if status_callback:
                status_callback(res)

            if not done:
                backoff_seconds = min(backoff_seconds * backoff_multiplier, maximum_backoff_seconds)
                await asyncio.sleep(backoff_seconds)

        return res
