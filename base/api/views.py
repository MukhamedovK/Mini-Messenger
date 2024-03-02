from rest_framework.views import APIView
from rest_framework.response import Response

from base.models import Room
from .serializers import GetRoomsSerializer


class GetRoutesView(APIView):
    def get(self, request):
        routes = [
            'GET /api',
            'GET /api/rooms',
            'GET /api/room/:id'
        ]
        return Response(routes)


class GetRoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = GetRoomsSerializer(instance=rooms, many=True)

        return Response(serializer.data)


class GetRoomView(APIView):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        serializer = GetRoomsSerializer(instance=room, many=False)

        return Response(serializer.data)

