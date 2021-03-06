import json
import logging
from .schema import schema
from django.test import override_settings
from graphene_django.utils.testing import GraphQLTestCase as GQLTestCase
from {{cookiecutter.project_slug}}.users.tests.factories import (
    UserFactory
)


@override_settings(GRAPHQL_JWT={
    'JWT_AUTH_HEADER_NAME': 'Authorization',
    'JWT_AUTH_HEADER_PREFIX': 'Bearer'
})
class GraphQLTestCase(GQLTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = "/"
    headers = {}

    def tearDown(self):
        UserFactory.reset_sequence()

    def _logging(self, query, result, variables={}):
        logging.info("""
            Query: {query}
            Variables: {variables}
            Expected: {result}
        """.format(
            query=query,
            variables=variables,
            result=result
        ))

    def _set_token(self, token=None):
        self.headers = {
            'Authorization': 'Bearer ' + token
        } if token else {}

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
