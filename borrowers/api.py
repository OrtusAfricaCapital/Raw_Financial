from rest_framework import status, generics
from rest_framework import response
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.generics import GenericAPIView
from django.core.exceptions import ObjectDoesNotExist


from .serializer import *
from .models import *

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def get_all_borrowers(request):
    if request.method == "GET":
        borrowers = Borrower.objects.all()
        if borrowers:
            serializer = BorrowerSerializer(borrowers, many=True)
            return Response(serializer.data)
        else:
            return Response({"erorr":"No Borrowers"}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "POST":
        serializer = BorrowerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"Successfully created Borrower"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":"Sorry, SOmething went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        


        

