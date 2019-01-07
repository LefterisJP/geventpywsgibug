import sys

import grequests
from flask import url_for

from example.api import APIServer, RestAPI


def api_url_for(api_server, endpoint, **kwargs):
    with api_server.flask_app.app_context():
        return url_for('v1_resources.{}'.format(endpoint), **kwargs)


if __name__ == '__main__':
    api_host = '127.0.0.1'
    api_port = 5004
    rest_api = RestAPI()
    server = APIServer(rest_api)
    server.flask_app.config['SERVER_NAME'] = 'localhost:{}'.format(api_port)
    server.start(api_host, api_port)

    request = grequests.get(
        api_url_for(
            server,
            'testcaseresource',
        ),
    )
    request.send().response
    server.stop()
    print('Finished succesfully')
    sys.exit(0)
