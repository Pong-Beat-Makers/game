from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import GameDataSerializer
from .models import GameDataModel
from config.verifying_user import verifying_user
from config.utils import get_token
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.

class GameDataListView(APIView):
    def get(self, request):
        try:
            verifying_user(get_token(request))
            id = request.GET['id']
            game_data_queryset = GameDataModel.objects.filter(
                Q(user1_id=id) | Q(user2_id=id)
            ).order_by('-created_at')

            if not game_data_queryset.exists():
                return Response({'error': 'data not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = GameDataSerializer(game_data_queryset, many=True,
                                            context={'id': id})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
