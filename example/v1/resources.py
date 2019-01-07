from flask import Blueprint
from flask_restful import Resource
from webargs.flaskparser import use_kwargs

from .encoding import TestcaseSchema


def create_blueprint():
    return Blueprint('v1_resources', __name__)


class BaseResource(Resource):
    def __init__(self, rest_api_object, **kwargs):
        super().__init__(**kwargs)
        self.rest_api = rest_api_object


class TestcaseResource(BaseResource):

    get_schema = TestcaseSchema

    @use_kwargs(get_schema)
    def get(self, **kwargs):
        return self.rest_api.test_case(**kwargs)
