import json
import logging
from graphene_django.utils.testing import GraphQLTestCase as GQLTestCase
from django.test.utils import override_settings
from .schema import schema
from {{cookiecutter.project_slug}}.users.tests.factories import (
    UserFactory
)
from datetime import timedelta


class GraphQLTestCase(GQLTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = "/"
    headers = {}

    def tearDown(self):
        UserFactory.reset_sequence()

    def logging(self, query, result, variables={}):
        logging.info("""
            Query: {query}
            Variables: {variables}
            Expected: {result}
        """.format(
            query=query,
            variables=variables,
            result=result
        ))

    def set_headers(self, token=None):
        self.headers = {
            'Authorization': 'Bearer ' + token
        } if token else {}

    @override_settings(DEBUG=True, GRAPHQL_JWT={
        'JWT_SECRET_KEY': 'KEY',
        'JWT_VERIFY_EXPIRATION': True,
        'JWT_AUTH_HEADER_NAME': 'Authorization',
        'JWT_AUTH_HEADER_PREFIX': 'Bearer',
        'JWT_EXPIRATION_DELTA': timedelta(days=30),
        'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=365),
    })
    def _execute_query(self, query, op_name, variables={}, should_fail=False):
        logging.disable(logging.CRITICAL)
        response = self.query(
            query=query,
            op_name=op_name,
            variables=variables,
            headers=self.headers
        )
        logging.disable(logging.NOTSET)
        content = json.loads(response.content)

        try:
            if should_fail:
                self.assertResponseHasErrors(response)
                return content['errors']
            else:
                self.assertResponseNoErrors(response)
                return content['data'][op_name]
        except Exception as e:
            print(content)
            raise e
