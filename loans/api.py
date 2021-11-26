from rest_framework import status, generics
from rest_framework import response
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.generics import GenericAPIView
from django.core.exceptions import ObjectDoesNotExist


from .models import *
from .serializer import *


@api_view(['GET','POST'])
@permission_classes([AllowAny])
def loan_request(request):
    if request.method == 'POST':
        loan_request = LoanRequestSerializer(data=request.data)
        if loan_request.is_valid():
            loan_request.save()
            return Response({"success":"Loan request received"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":"Oops, Field error"}, status=status.HTTP_400_BAD_REQUEST)


