from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Welcome(APIView):
    def get(self, request):
        return Response("Welcome to the Library Management System", status=status.HTTP_200_OK)