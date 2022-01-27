from django.shortcuts import render
from .models import User


from rest_framework import generics, status
from rest_framework.authentication import AUTH_HEADER_TYPES
from rest_framework import exceptions
from rest_framework.response import Response

# Create your views here.



def user_view():
    users = User.objects.all()
    context = {
        'users': users
    }
    return render('user.html', context)

class TokenView(generics.GenericView):
    permission_classes = ()
    authentication_classes = ()
    
    serializer_class = None
    
    def get_authenticate_header(self, request):
        return "{} realm='{}'".format(AUTH_HEADER_TYPES[0], self.www_authenticate_realm,)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    