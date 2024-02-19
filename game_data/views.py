from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import GameDataSerializer

# Create your views here.

class GameDataAPIView(APIView):
    serializer_class = GameDataSerializer
    def get(self, request):
        serializer = self.serializer_class(data=request.data)
