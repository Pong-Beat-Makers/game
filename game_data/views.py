from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import GameDataSerializer
from .models import GameDataModel
from config.verifying_user import verifying_user
from config.utils import get_token

# Create your views here.

class GameDataListView(APIView):
    def get(self, request):
        try:
            # verifying_user(get_token(request))
            nickname = request.GET['nickname']
            game_data_queryset = GameDataModel.objects.filter(
                Q(user1_nickname=nickname) | Q(user2_nickname=nickname)
            ).order_by('-created_at')

            if not game_data_queryset.exists():
                return Response({'error': 'data not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = GameDataSerializer(game_data_queryset, many=True,
                                            context={'nickname': request.GET['nickname']})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
