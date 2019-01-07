from gevent import monkey

monkey.patch_all()

if True:
    import logging

    from flask import Flask
    from flask_restful import Api
    from gevent.pywsgi import WSGIServer

    from example.v1.resources import TestcaseResource, create_blueprint

logger = logging.getLogger(__name__)

URLS_V1 = [
    ('/test_case', TestcaseResource),
]


def restapi_setup_urls(flask_api_context, rest_api, urls):
    for route, resource_cls in urls:
        flask_api_context.add_resource(
            resource_cls,
            route,
            resource_class_kwargs={'rest_api_object': rest_api},
        )


class APIServer(object):

    _api_prefix = '/api/1'

    def __init__(self, rest_api):
        flask_app = Flask(__name__)
        blueprint = create_blueprint()
        flask_api_context = Api(blueprint, prefix=self._api_prefix)

        restapi_setup_urls(
            flask_api_context,
            rest_api,
            URLS_V1,
        )

        self.rest_api = rest_api
        self.flask_app = flask_app
        self.blueprint = blueprint
        self.flask_api_context = flask_api_context

        self.wsgiserver = None
        self.flask_app.register_blueprint(self.blueprint)

    def start(self, host='127.0.0.1', port=5001):
        self.wsgiserver = WSGIServer((host, port), self.flask_app, log=logger, error_log=logger)
        # If the logger is not specified then we get the expected result!
        # self.wsgiserver = WSGIServer((host, port), self.flask_app)
        self.wsgiserver.start()

    def stop(self, timeout=5):
        if getattr(self, 'wsgiserver', None):
            self.wsgiserver.stop(timeout)
            self.wsgiserver = None


class RestAPI(object):
    """ The Object holding the logic that runs inside all the API calls"""
    def __init__(self):
        self.apiversion = '1'

    def test_case(self):
        raise ValueError('This will trigger stack overflow error and segfault python interpreter')
        return 42
