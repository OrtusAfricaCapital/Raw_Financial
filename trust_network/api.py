from rest_framework import status, generics
from rest_framework import response
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from django.core.exceptions import ObjectDoesNotExist

import trust_network

from .models import *
from .serializer import *


@api_view(['GET','POST'])
@permission_classes([AllowAny])
def trustnetwork_apiview(request):
    if request.method == 'GET':
        trust_network = TrustNetwork.objects.all()
        if trust_network:
            serializer = TrustNetworkSerializer(trust_network, many=True)
            return Response(serializer.data)
        else:
            return Response({"error":"No trust networks"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        serializer = TrustNetworkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"Successfully created Trust Network"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":"Sorry, SOmething went wrong"}, status=status.HTTP_400_BAD_REQUEST)