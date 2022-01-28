from django.shortcuts import render
from .models import User

from rest_framework.decorators import api_view, renderer_classes
from rest_framework import generics
from rest_framework. permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt import exceptions
from rest_framework.response import Response
from .serializers import TokenObtainSerializer, TokenObtainPairSerializer
from rest_framework import status
from django.http import JsonResponse
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
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
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ProtectedView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    
    def get_queryset(self):
        rss = {
        "chaley": "brooooo",
        "geeee": "geeeeee"
        }
        return rss

  
class Not_ProtectedView(generics.ListAPIView):
     queryset = {
         "chaley": "brooooo",
         "geeee": "geeeeee"
     }





@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def not_protected_view(request):
    response = {
        "good": "you made it",
        "boy": "girl"
    }
    return Response(response, status=status.HTTP_200_OK)