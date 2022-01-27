from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _


class PasswordField(serializers.Field):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})
        kwargs['style']['input_type'] = 'password'
        
        super().__init__(*args, **kwargs)    

class TokenObtainSerializer(serializers.CharField):
    username_field = get_user_model().USERNAME_FIELD
    
    default_error_messages = {
        "no_active_account": _("No active account available  o")
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields[self.username_field] = serializers.CharField()
        self.fields["password"] = PasswordField()
    
    def validate(self, attrs):
        