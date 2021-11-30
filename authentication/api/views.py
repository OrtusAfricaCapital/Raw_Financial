from rest_framework import status, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.schemas import get_schema_view
#from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


from authentication.models import *
from authentication.api.serializer import *
from rest_framework.authtoken.models import Token
from authentication.authentication import token_expire_handler, expires_in
from cloudinary import uploader



#user create and list view
class UserCreateListView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request, format=None):
        context = {}
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            context['message'] = "succesfully created account"
            context['uuid'] = account.uuid
            token = Token.objects.get(user=account).key
            context['token'] = token
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        queryset = User.objects.all()
        serializer = RegistrationSerializer(queryset, many=True, context={'request':request} )
        return Response(serializer.data)

#login view
class LoginToken(ObtainAuthToken):
   """Return User Info along with token"""
   def post(self, request, *arg, **kwarg):

       serializer = self.serializer_class(data=request.data, context={'request':request})
       if serializer.is_valid():
           user = serializer.validated_data['user']
           token = Token.objects.get(user=user)
           is_expred, token = token_expire_handler(token)
           #profile = AccountProfile.objects.get(user=user)
           return Response({
               'uuid':user.uuid,
               'token':token.key,
               'expires_in':expires_in(token),
           })
       return Response({"error_message":"Invalid email or password credentials"}, status=status.HTTP_404_NOT_FOUND)
        


@api_view(['GET','PUT','DELETE', 'PATCH'])
def UserDetail(request, pk):
    #check if object exists
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'message':'Wrong credentials'})
        #check for logged in user
    if user != request.user:
        return Response({'message':'Wrong credentials'})
        #else perform the following actions
    if request.method == "GET": 
        serializer = RegistrationSerializer(user, context={'request':request})
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = RegistrationSerializer(user, data=request.data, partial=True, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        user.delete()
        return Response({"message":"user has been deleted"}, status=status.HTTP_204_NO_CONTENT) 


"""
@permission_classes([IsAuthenticated])
class AccountTeamView(viewsets.ModelViewSet):
    queryset = AccountTeams.objects.all()
    serializer_class = AccountTeamsSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)     


@api_view(['PUT', 'GET'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def updatepic_view(request, pk):
    try:
        profile_pic = AccountProfilePic.objects.get(pk=pk, user=request.user)
    except AccountProfilePic.DoesNotExist:
        return Response({"error":"Can't update profile picture with these credentials"})
    if request.method == "PUT":
        
        serializer = AccountProfilePicSerializer(instance=profile_pic, data=request.FILES, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            #upload_image = uploader.upload(pic)
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == "GET":
        get_pic = AccountProfilePic.objects.get(pk=pk)
        serializer = AccountProfilePicSerializer(get_pic, many=False, context={'request':request})
        return Response(serializer.data)

"""
    