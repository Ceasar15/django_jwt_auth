import jwt
from django.utils.translation import gettext_lazy as _
from jwt import InvalidAlgorithmError, InvalidTokenError, PyJWKClient, algorithms
from rest_framework_simplejwt import exceptions

ALLOWED_ALGORITHMS = (
    "HS256",
)

class TokenBackend:
    def __init__(self, algorithm, signing_key=None, verifying_key="", audience=None, issuer=None, jwk_url: str = None, leeway=0):
        self._validate_algorithm(algorithm)
        
        self.algorithm = algorithm
        self.signing_key = signing_key
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
    
            
        


