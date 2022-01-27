from datetime import timedelta
from uuid import uuid4
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _
from rest_framework.settings import api_settings
from django.utils.module_loading import import_string

class Token:
    
    token_type = None
    lifetime = None
    def __init__(self, token=None, verify=True):
        
        if self.token_type is None:
            raise exceptions.InvalidTokenError(_("Cannot create token with no type or lifetime"))
        
        self.token = token
        self.current_time = None
        
        if token is not None:
            token_backend = self.get_token_backend()
            
            try:
                self.payload = token_backend.decode(token, verify=verify)
            except exceptions.TokenBackendError:
                raise exceptions.TokenError(_("Token is invalid or expired"))
            
            if verify:
                self.verify()
            
        else:
            self.payload = {api_settings.TOKEN_TYPE_CLAIM: self.token_type}
            
            # Set "exp" and "iat" claims with default value
            self.set_exp(from_time=self.current_time, lifetime=self.lifetime)
            self.set_iat(at_time=self.current_time)

            # Set "jti" claim
            self.set_jti()
            
    def __str__(self):
        """
        Signs and returns a token as a base64 encoded string.
        """
        return self.get_token_backend().encode(self.payload)
    
    def set_jti(self):
        self.payload[api_settings.JTI_CLAIM] = uuid4().hex
    
    def set_exp(self, claim='exp', lifetime=None, from_time=None):
        if from_time is None:
            from_time = self.current_time
            
        if lifetime is None:
            lifetime = self.lifetime
        
    
    def verify_token_type(self):
        try:
            token_type = self.payload[api_settings.TOKEN_TYPE_CLAIM]
        except KeyError:
            raise exceptions.TokenError(_("Token has no type"))
        
    @classmethod
    def for_user(cls, user):
        user_id = getattr(user, api_settings.USER_ID_FIELD)
        if not isinstance(user_id, int):
            user_id = str(user_id)
            
        token = cls()
        token[api_settings.USER_ID_CLAIM] = user_id

        return token
    
    _token_backend = None
    
    def get_token_backend(self):
        if self._token_backend is None:
            self._token_backend = import_string(
                "rest_framework_simplejwt.state.token_backend"
            )            
        return self._token_backend
    
class AccessToken(Token):
    token_type = "access"
    lifetime = api_settings.ACCESS_TOKEN_LIFETIME
    
    
class RefreshToken(Token):
    token_type = "refresh"
    lifetime = api_settings.REFRESH_TOKEN_LIFETIME
    
    no_copy_claims = (
        api_settings.TOKEN_TYPE_CLAIM,
        'exp',
        api_settings.JTI_CLAIM,
        'jti'
    )
    
    @property
    def access_token(self):
        access = AccessToken()
        
        access.set_exp(from_time=self.current_time)