import jwt
from django.utils.translation import gettext_lazy as _
from jwt import InvalidAlgorithmError, InvalidTokenError, PyJWKClient, algorithms
from rest_framework_simplejwt import exceptions
from .config import ALLOWED_ALGORITHMS


class TokenBackend:
    def __init__(self, algorithm, signing_key=None, verifying_key="", audience=None, issuer=None, jwk_url: str = None, leeway=0):
        self._validate_algorithm(algorithm)
        
        self.algorithm = algorithm
        self.signing_key = str(signing_key)
        self.verifying_key = verifying_key
        self.audience = audience
        self.issuer = issuer
        self.jwks_client = PyJWKClient(jwk_url) if jwk_url else None
        self.leeway = leeway
        
    def _validate_algorithm(self, algorithm):
        
        if algorithm not in ALLOWED_ALGORITHMS:
            raise exceptions.TokenBackendError(_("Invalid algorithm: {}".format(algorithm)))
        
        if algorithm in algorithms.requires_cryptography and not algorithms.has_crypto:
            raise exceptions.TokenBackendError(_("You must have cryptography support to use {}"), algorithm)
        
    def get_verify_algorithm(self, token):
        if self.algorithm.startswith("HS"):
            return self.signing_key
        
        if self.jwks_client:
            return self.jwks_client.get_signing_key_from_jwt(token).key
        
        return self.verifying_key
    
    def encode(self, payload):
        jwt_payload = payload.copy()
        
        if self.audience is not None:
            jwt_payload["aud"] = self.audience
            
        if self.issuer is not None:
            jwt_payload["iss"] = self.issuer
        
        print(type(jwt_payload))
        print(type(self.signing_key))
        print(type(self.algorithm))
        token = jwt.encode(jwt_payload, self.signing_key, algorithm=self.algorithm)
        if isinstance(token, bytes):
            return token.decode("utf-8")
        
        print(token)
        return token            
        
    def decode(self, token, verify=True):
        try:
            return jwt.decode(
                token,
                self.get_vverifying_key(token),
                audinece =self.audience,
                issuer=self.issuer,
                leeway=self.leeway,
                options={
                    "verify_aud": self.audience is not None,
                    "verify_signature": verify
                    },
            )
        except jwt.exceptions.InvalidAlgorithmError as ex:
            raise exceptions.TokenBackendError(_("INvalid algorithm specified")) from ex
        except jwt.exceptions.InvalidTokenError:
            raise exceptions.TokenBackendError(_("Token is invalid or expired"))


