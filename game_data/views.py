from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import GameDataSerializer
from .models import GameDataModel
from operator import attrgetter

# Create your views here.

class GameDataListView(APIView):
    def get(self, request):
        nickname = request.GET.get('nickname')
        game_data_queryset = GameDataModel.objects.filter(
            Q(user1_nickname=nickname) | Q(user2_nickname=nickname)
        ).order_by('-created_at')

        if not game_data_queryset.exists():
            return Response({'error': 'data not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GameDataSerializer(game_data_queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
