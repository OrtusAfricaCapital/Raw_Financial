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
@permission_classes([IsAuthenticated])
def loan_request(request):
    context = {}
    if request.method == 'POST':
        data = request.data
        channel_borrower_id = data['channel_borrower_uid']
        #get borrower
        try:
            borrower_query = Borrower.objects.get(channel_borrower_uid=channel_borrower_id)
            if borrower_query:
                loan_request = LoanRequestSerializer(data=request.data)
                if loan_request.is_valid():
                    loan_request = loan_request.save()
                    lr = LoanRequest.objects.get(id=loan_request.id)
                    LoanRequestStatus.objects.create(
                        loan_id = lr,
                        loan_status_description = "Initial Description",
                    )
                    context['succes'] = "Loan request received"
                    context['loan_request_id'] = loan_request.loan_request_uid
                    return Response(context, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error":"Oops, Field error"}, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response({"error":"This borrower doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
                
        except Borrower.DoesNotExist:
            return Response({"error":"Borrower ID not recorgnized"}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        get_loan_request = LoanRequest.objects.all()
        if get_loan_request:
            serializer = LoanRequestSerializer(get_loan_request, many=True)
            return Response(serializer.data)
        else:
            return Response({"error":"no loan requests"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def loan_status(request, lr_id):
    if request.method == 'GET':
        try:
            loan_request = LoanRequest.objects.get(loan_request_uid=lr_id)
            print(loan_request.id)
            
            try:

                loan_status = LoanRequestStatus.objects.get(loan_id=loan_request.id)
                if loan_status:
                    serializer = LoanStatusSerializer(loan_status)
                    return Response(serializer.data)
                else:
                    return Response({"error":"No status Change"}, status=status.HTTP_400_BAD_REQUEST)
            except LoanRequestStatus.DoesNotExist:
                return Response({"error":"Loan Status doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        except LoanRequest.DoesNotExist:
            return Response({"error":"Loan request doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)



        


