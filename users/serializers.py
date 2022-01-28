from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from .tokens import AccessToken, RefreshToken

class PasswordField(serializers.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})
        kwargs['style']['input_type'] = 'password'
        kwargs["write_only"] = True

        super().__init__(*args, **kwargs)


class TokenObtainSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD

    default_error_messages = {
        "no_active_account": _("No active account available  o")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["password"] = PasswordField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"]
        }

        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        return {}
    
class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        print("data serial", data)
        print("userrrr", self.user)
        refresh = self.get_token(self.user)
        
        data["refresh"] = str(refresh) 
        data["access"] = str(refresh.access)        
        
        return data