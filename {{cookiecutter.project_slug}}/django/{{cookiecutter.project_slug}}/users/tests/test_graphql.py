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

    def login_email(self, **kwargs):
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
            'fullName': 'John Doe'
        }
        self._logging(
            query="createUser",
            variables=variables,
            result="The user is created"
        )
        self.create_user(variables=variables)

        logging.info("* I want to login with my new user.")
        variables = {
            'username': "email@email.com",
            'password': "password2"
        }
        self._logging(
            query="loginEmail",
            variables=variables,
            result="I can't login because I set a wrong password"
        )
        self.login_email(variables=variables, should_fail=True)

        variables = {
            'username': "email@email.com",
            'password': "password"
        }
        self._logging(
            query="loginEmail",
            variables=variables,
            result="I login successfully now that I put the right password"
        )
        response = self.login_email(variables=variables)

        logging.info("* I now want to get my profile.")
        self._logging(
            query="userProfile",
            result="It should fail because I didn't put my token"
        )
        self.user_profile(should_fail=True)
        self._set_token(token=response['token'])
        self._logging(
            query="userProfile",
            result="It should work because I added my token in the headers"
        )
        self.user_profile()
