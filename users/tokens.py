from datetime import timedelta
from uuid import uuid4
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string
from .utils import datetime_from_epoch, datetime_to_epoch, aware_utcnow
from .config import ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME, TOKEN_TYPE_CLAIM, JTI_CLAIM, USER_ID_FIELD, USER_ID_CLAIM

class Token:
    
    token_type = None
    lifetime = None
    def __init__(self, token=None, verify=True):
        
        if self.token_type is None:
            raise exceptions.InvalidTokenError(_("Cannot create token with no type or lifetime"))
        
        self.token = token
        self.current_time = aware_utcnow()
                
        if token is not None:
            token_backend = self.get_token_backend()
            
            try:
                self.payload = token_backend.decode(token, verify=verify)
            except exceptions.TokenBackendError:
                raise exceptions.TokenError(_("Token is invalid or expired"))
            
            if verify:
                self.verify()
            
        else:
            self.payload = {TOKEN_TYPE_CLAIM: self.token_type}
            
            # Set "exp" and "iat" claims with default value
            self.set_exp(from_time=self.current_time, lifetime=self.lifetime)
            self.set_iat(at_time=self.current_time)

            # Set "jti" claim
            self.set_jti()
            
    def __str__(self):
        """
        Signs and returns a token as a base64 encoded string.
        """
        print(self.payload)
        return self.get_token_backend().encode(self.payload)
    
    def set_jti(self):
        self.payload[JTI_CLAIM] = uuid4().hex
    
    def set_exp(self, claim='exp', lifetime=None, from_time=None):
        if from_time is None:
            from_time = self.current_time
            
        if lifetime is None:
            lifetime = self.lifetime
    
    def check_exp(self, claim='exp', current_time=None):
        if current_time is None:
            current_time = self.current_time
            
        try:
            claim_value = self.payload[claim] 
        except exceptions.KeyError:
            raise exceptions.TokenError(_("Token has no {} claim"))
        
        claim_time = datetime_from_epoch(claim_value)
        if claim_time <= current_time:
            raise exceptions.TokenError(_("Token {} claim has expired"), claim)
           
    def set_iat(self, claim='iat', at_time=None):
        if at_time is None:
            at_time = self.current_time
            
        self.payload[claim] = datetime_to_epoch(at_time)
    
    def get(self, key, default=None):
        return self.payload.get(key, default)
    
    def verify_token_type(self):
        try:
            token_type = self.payload[TOKEN_TYPE_CLAIM]
        except KeyError:
            raise exceptions.TokenError(_("Token has no type"))
        
    @classmethod
    def for_user(cls, user):
        user_id = getattr(user, USER_ID_FIELD)
        if not isinstance(user_id, int):
            user_id = str(user_id)
        
        token = cls()
        print("dfsdfsdfsdfsd", token)
        token[USER_ID_CLAIM] = str(user_id)

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
    lifetime = ACCESS_TOKEN_LIFETIME
    
    
class RefreshToken(Token):
    token_type = "refresh"
    lifetime = REFRESH_TOKEN_LIFETIME
    
    no_copy_claims = (
        TOKEN_TYPE_CLAIM,
        'exp',
        JTI_CLAIM,
        'jti'
    )
    
    @property
    def access_token(self):
        access = AccessToken()
        
        access.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value

        return access;        
        