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
@permission_classes([IsAuthenticated])
def trustnetwork_apiview(request):
    if request.method == 'GET':
        trust_network = TrustNetwork.objects.all()
        if trust_network:
            serializer = TrustNetworkSerializer(trust_network, many=True)
            return Response(serializer.data)
        else:
            return Response({"error":"No trust networks"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        context = {}
        data = request.data
        tn_name = data['Name']
        get_tn = TrustNetwork.objects.filter(Name=tn_name)
        if get_tn:
            return Response({"error":"Sorry, Trust Network already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = TrustNetworkSerializer(data)
            if serializer.is_valid():
                serializer.save()
                uid = serializer.data.get('trustnetwork_uid', None)
                tn = TrustNetwork.objects.get(trustnetwork_uid=uid)
                context['success'] = "Successfully created Trust Network"
                context['trust_network_id'] = tn.id
                
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                return Response({"error":"Sorry, SOmething went wrong"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def trust_status(request, tn_id):
    if request.method == 'GET':
        try:
            tn_request = TrustNetwork.objects.get(trustnetwork_uid=tn_id)
            #print(tn_request.id)
            
            try:

                tn_status = TrustNetworkStatus.objects.get(tn_id=tn_request.id)
                if tn_status:
                    serializer = TrustNetworkStatusSerializer(tn_status)
                    return Response(serializer.data)
                else:
                    return Response({"error":"No status Change"}, status=status.HTTP_400_BAD_REQUEST)
            except TrustNetworkStatus.DoesNotExist:
                return Response({"error":"Trust Network Status doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        except TrustNetworkStatus.DoesNotExist:
            return Response({"error":"Trust Network doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)