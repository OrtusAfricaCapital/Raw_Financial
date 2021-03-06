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
@permission_classes([IsAuthenticated])
def get_all_borrowers(request):
    context = {}
    if request.method == "GET":
        borrowers = Borrower.objects.all()
        if borrowers:
            serializer = BorrowerSerializer(borrowers, many=True)
            return Response(serializer.data)
        else:
            return Response({"erorr":"No Borrowers"}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "POST":
        data = request.data
        cbi = data['channel_borrower_uid']
    
        borrower = Borrower.objects.filter(channel_borrower_uid=cbi)
        if borrower:
            return Response({"error":"Borrower already exists"}, status=status.HTTP_201_CREATED)
        else:
            serializer = BorrowerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"success":"Successfully created Borrower"}, status=status.HTTP_201_CREATED)
            else:
                context['error'] = "Oops, Field Error"
                context['description'] = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        


        

