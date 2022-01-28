from django.shortcuts import render
from .models import User


from rest_framework import generics
# from rest_framework.authentication import AUTH_HEADER_TYPES
# from rest_framework import exceptions
from rest_framework_simplejwt import exceptions
from rest_framework.response import Response
from .serializers import TokenObtainSerializer, TokenObtainPairSerializer
from rest_framework import status
# Create your views here.



# def user_view(request):
#     users = User.objects.all()
#     context = {
#         'users': users
#     }
#     return render(request, context)

class TokenView(generics.CreateAPIView):
    permission_classes = ()
    authentication_classes = ()
    
    serializer_class = TokenObtainPairSerializer
    
    def get_authenticate_header(self, request):
        return "{} realm='{}'".format(self.www_authenticate_realm,)
    
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    