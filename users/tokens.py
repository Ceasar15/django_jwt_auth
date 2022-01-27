from datetime import timedelta
from uuid import uuid4
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _

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
            self.payload = {}
            
            
            
            
            
            
            