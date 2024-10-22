import logging
import time
import jwt
import requests
from app.core.config import settings  # FastAPI 설정 파일 사용

logger = logging.getLogger('auth')

class RequestData_apple:
    def __init__(self, data) -> None:
        self.__authorization_code = data.get('authorizationCode', '')
        self.__authorization_scopes = data.get('authorizdScopes', [])
        self.__email = data.get('email', '')
        self.__fullname = data.get('fullName', {})
        self.__identity_token = data.get('identityToken', '')
        self.__nonce = data.get('nonce', '')
        self.__real_user_status = data.get('realUserStatus', 0)
        self.__state = data.get('state', None)
        self.__user = data.get('user', '')

    @property
    def authorization_code(self):
        return self.__authorization_code

    @authorization_code.setter
    def authorization_code(self, value):
        if value == '':
            raise ValueError('Authorization code is not setted')
        self.__authorization_code = value

    @property
    def authorization_scopes(self):
        return self.__authorization_scopes

    @authorization_scopes.setter
    def authorization_scopes(self, value):
        self.__authorization_scopes = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def fullname(self):
        return self.__fullname

    @fullname.setter
    def fullname(self, value):
        self.__fullname = value

    @property
    def identity_token(self):
        return self.__identity_token

    @identity_token.setter
    def identity_token(self, value):
        self.__identity_token = value

    @property
    def nonce(self):
        return self.__nonce

    @nonce.setter
    def nonce(self, value):
        self.__nonce = value

    @property
    def real_user_status(self):
        return self.__real_user_status

    @real_user_status.setter
    def real_user_status(self, value):
        self.__real_user_status = value

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        self.__user = value

    def __str__(self) -> str:
        ret = 'Apple auth data\n'
        ret += f'Auth code: {self.authorization_code}\n'
        ret += f'authorization_scopes: {self.authorization_scopes}\n'
        ret += f'email: {self.email}\n'
        ret += f'fullname: {self.fullname}\n'
        ret += f'identity_token: {self.identity_token}\n'
        ret += f'nonce: {self.nonce}\n'
        ret += f'real_user_status: {self.real_user_status}\n'
        ret += f'state: {self.state}\n'
        ret += f'user: {self.user}\n'
        return ret


class Auth_apple:
    client_id = settings.APPLE_CLIENT_ID
    private_key = settings.APPLE_CERT_KEY_PATH
    app_id = settings.APPLE_MEMBER_ID
    key_id = settings.APPLE_KEY_ID

    @classmethod
    def get_client_secret(cls):
        additional_headers = {'kid': cls.key_id}
        iat = time.time()
        payload = {
            'iss': cls.app_id,
            'iat': iat,
            'exp': iat + 3600,
            'aud': 'https://appleid.apple.com',
            'sub': cls.client_id
        }
        client_secret = jwt.encode(payload, cls.private_key.encode(), headers=additional_headers, algorithm='ES256')
        return client_secret

    @classmethod
    def verify_token(cls, authorization_code):
        client_secret = cls.get_client_secret()
        auth_payload = {
            'client_id': cls.client_id,
            'client_secret': client_secret,
            'code': authorization_code,
            'grant_type': 'authorization_code',
        }
        res = requests.post("https://appleid.apple.com/auth/token", data=auth_payload)
        try:
            res.raise_for_status()
            return res.json(), True
        except requests.exceptions.HTTPError as err:
            logger.error(err)
            return res.json(), False

    @classmethod
    def decode_jwt_token(cls, jwt_data):
        return jwt.decode(jwt_data, algorithms=settings.APPLE_ALGORITHM, audience=cls.client_id, options={"verify_signature": False})
