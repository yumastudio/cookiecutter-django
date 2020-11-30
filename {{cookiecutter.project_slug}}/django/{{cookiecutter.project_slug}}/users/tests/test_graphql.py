import logging
from config.testing import GraphQLTestCase
from .factories import UserFactory

USERS_COUNT = 10


class UserTestCase(GraphQLTestCase):
    def setUp(cls):
        UserFactory.create_batch(USERS_COUNT)

    def create_user(self, **kwargs):
        query = '''
            mutation createUser(
                $email: String!,
                $password: String!,
                $fullName: String!) {
                createUser(
                    email: $email,
                    password: $password,
                    fullName: $fullName) {
                    user {
                        id
                        email
                    }
                }
            }
        '''
        return self._execute_query(
            query=query,
            op_name="createUser",
            **kwargs
        )

    def get_user_profile(self, **kwargs):
        query = '''
            query userProfile {
                userProfile{
                    id
                    email
                    firstName
                    lastName
                }
            }
        '''
        return self._execute_query(
            query=query,
            op_name="userProfile",
            **kwargs
        )

    def login(self, **kwargs):
        query = '''
            mutation loginEmail(
                $username: String!,
                $password: String!
            ) {
                loginEmail(
                    username: $username,
                    password: $password
                ) {
                    token
                    user {
                        id
                        email
                    }
                }
            }
        '''
        return self._execute_query(
            query=query,
            op_name="loginEmail",
            **kwargs
        )

    def verify_token(self, **kwargs):
        query = '''
            mutation verifyToken(
                $token: String!) {
                verifyToken(
                    token: $token) {
                    payload
                }
            }
        '''
        return self._execute_query(
            query=query,
            op_name="verifyToken",
            **kwargs
        )

    def test_user(self):
        logging.info("* I want to create a new user.")
        variables = {
            'email': "email@email.com",
            'password': "password",
            'full_name': 'John Doe'
        }
        self.logging(
            query="seoCities",
            variables=variables,
            result="The user is created"
        )
        self.create_user(variables=variables)
