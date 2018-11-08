import requests
import sys
import jwt
from accounts.models import ListUser


class Auth0AuthenticationBackend(object):
    # Send the assertion to Auth0's verifier service
    def authenticate(self, code):
        """data = {'response_type': 'code',  # Can be token
                'client_id': '6gT7WSD5P4pr8cswROuvKV0FF_K2dW09',
                'redirect_uri': 'http://127.0.0.1:8000',
                'scope': 'openid'
                }
        print('sending to Auth0', data, file=sys.stderr)
        resp = requests.get('https://tdd-dubris.eu.auth0.com/authorize?',
                            params=data)
        print('got the code', resp.content, file=sys.stderr)"""

        # Did the verifier respond?
        print('got the code\n', file=sys.stderr)

        # Get the token
        data = {'grant_type': 'authorization_code',  # Can be code
                'client_id': '6gT7WSD5P4pr8cswROuvKV0FF_K2dW09',
                'client_secret': 'oWLF8fbCyMKulRbxS9avuvlXg-tNwhBD7SkeTiZ7IpjCeYm9dxC-7LhNMWhxOKzG',
                'code': code,
                'redirect_uri': 'http://127.0.0.1:8000',
                'audience': 'https://tdd-dubris.eu.auth0.com/userinfo'
                }
        headers = {'cotent-type': 'application/json'}
        print('sending code to Auth0\n', data, file=sys.stderr)
        resp = requests.post('https://tdd-dubris.eu.auth0.com/oauth/token',
                             data=data,
                             headers=headers)
        token = resp.json()
        print('got the token\n', token, '\n', file=sys.stderr)

        # Get the user info and check the email is valid
        user_info = jwt.decode(token['id_token'], verify=False)
        print('got the user info\n', user_info, '\n', file=sys.stderr)

        # Did the verifier respond?
        if user_info['email_verified'] is True:
            # Check if the assertion was valid
            email = user_info['email']
            try:
                return self.get_user(email)
            except ListUser.DoesNotExist:
                return ListUser.objects.create(email=email)

    def get_user(self, email):
        return ListUser.objects.get(email=email)
