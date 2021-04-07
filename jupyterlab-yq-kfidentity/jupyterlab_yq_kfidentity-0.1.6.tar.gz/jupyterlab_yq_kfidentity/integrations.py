import requests
import xmltodict
import json
import jwt as pyjwt
import os

from jupyter_server.base.handlers import APIHandler
from tornado.log import app_log
import tornado.httpclient as httpclient
from jupyter_server.utils import url_path_join
from datetime import datetime

JWT_PATH = '/yq/jwt.txt'
MINIO_PATH = '/yq/minio.json'
JWT_HEADER = os.getenv('JWT_HEADER', default='userid-token')


def get_jwt():
    try:
        with open(JWT_PATH, 'r') as jwt:
            out = jwt.read()
            jwt.close()
            return out
    except OSError:
        app_log.debug('JWT is not created yet or failed to be fetched.')
        return None


def has_expired(token, alg='HS512'):
    decoded = pyjwt.decode(token, options={"verify_signature": False}, algorithms=alg)
    jwt_expired_date = datetime.fromtimestamp(int(decoded['exp']))
    now = datetime.now()
    return jwt_expired_date < now


class YqKfIdentity(APIHandler):
    def post(self):
        headers = self.request.headers
        jwt = get_jwt()

        if jwt is None or has_expired(jwt, alg='RS256'):
            if JWT_HEADER in headers:
                with open(JWT_PATH, 'w') as out:
                    out.write(headers[JWT_HEADER])
                    out.close()
            else:
                app_log.warn('There is no JWT token in the headers')
                self.set_status(500)
            self.finish(f"JWT Found: {headers[JWT_HEADER]}")
        else:
            self.finish('Kubeflow JWT is valid and not expired.')


class YqMinioIntegration(APIHandler):
    """
        In this integration we expose /yqid/minio to authenticate against Minio using Azure AD JWT,
        and then create a temporary user. Minio returns us XML with Access/Secret key and Session Token,
        we write that credentials into ~/.aws/credentials and IBM Jupyterlab S3 Browser should use them later.
    """
    async def post(self):
        jwt = get_jwt()
        if jwt is not None:
            # Check if AWS Session Token is there and not expired
            if 'AWS_SESSION_TOKEN' in os.environ and not has_expired(os.environ['AWS_SESSION_TOKEN']):
                await self.finish('Minio credentials are still valid.')
            else:
                params = (
                    ('Action', 'AssumeRoleWithWebIdentity'),
                    ('DurationSeconds', '3600'),
                    ('Version', '2011-06-15'),
                    ('WebIdentityToken', jwt),
                )

                response = requests.post('http://yq-storage-viewer.yq:9000/', params=params)
                if response.status_code == 200:
                    minio_response = json.loads(json.dumps(xmltodict.parse(response.content)))

                    credentials = \
                        minio_response['AssumeRoleWithWebIdentityResponse']['AssumeRoleWithWebIdentityResult'][
                            'Credentials']

                    os.environ['AWS_SESSION_TOKEN'] = credentials['SessionToken']
                    # Send POST to authenticate inside IBM Jupyterlab S3
                    headers = self.request.headers
                    cookies = self.request.cookies
                    token   = str(cookies['_xsrf']).split('=')[1]
                    #headers.add('X-XSRFToken', token)
                    headers.add('Content-Type', 'application/json')
                    data = f'{{"client_id":"{credentials["AccessKeyId"]}",' \
                           f'"client_secret":"{credentials["SecretAccessKey"]}",' \
                           f'"endpoint_url":"http://yq-storage-viewer.yq:9000",' \
                           f'"session_token":"{credentials["SessionToken"]}"}}'

                    http_client = httpclient.AsyncHTTPClient()
                    try:
                        response = await http_client.fetch(f"http://localhost:8888{os.environ['NB_PREFIX']}/jupyterlab_s3_browser/auth?_xsrf={token}",
                                                           method="POST", headers=headers, body=data)
                        with open(MINIO_PATH, 'w') as out:
                            out.write(data)
                            out.close()

                        aws_creds = f'''
[default]
aws_access_key_id = {credentials["AccessKeyId"]}
aws_secret_access_key = {credentials["SecretAccessKey"]}
aws_session_token = {credentials["SessionToken"]}
                        '''
                        aws_creds_file = os.path.expanduser('~/.aws/credentials')
                        with open(aws_creds_file, 'w') as out:
                            out.write(aws_creds)
                            out.close()
                    except httpclient.HTTPError as e:
                        # HTTPError is raised for non-200 responses; the response
                        # can be found in e.response.
                        app_log.error("Error: " + str(e))
                        self.set_status(500)
                    except Exception as e:
                        # Other errors are possible, such as IOError.
                        app_log.error("Error: " + str(e))
                        self.set_status(500)
                    http_client.close()
                    await self.finish(f"Minio credentials: {credentials}")
                else:
                    app_log.error(f'Failed to create STS credentials in Minio: {response.content}')
                    self.set_status(500)


def setup_handlers(web_app):
    """
    Setups all of the YQ ID integrations.
    Every handler is defined here to be integrated with JWT.
    """
    host_pattern = ".*"

    # add the baseurl to our paths
    base_url = web_app.settings["base_url"]
    handlers = [
        (url_path_join(base_url, "yqid", "sync"), YqKfIdentity),
        (url_path_join(base_url, "yqid", "minio"), YqMinioIntegration),
    ]

    web_app.add_handlers(host_pattern, handlers)
