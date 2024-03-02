from rest_framework.serializers import ModelSerializer
from datetime import datetime

from django.contrib.auth.models import User
from base.models import Room, Topic


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['name']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class GetRoomsSerializer(ModelSerializer):
    host = UserSerializer()
    topic = TopicSerializer()
    participants = UserSerializer(many=True)

    class Meta:
        model = Room
        fields = '__all__'

    def to_representation(self, instance):
        redata = super().to_representation(instance)
        redata['created_at'] = datetime.strftime(instance.created_at, '%d-%m-%Y %H:%M:%S')
        redata['updated_at'] = datetime.strftime(instance.updated_at, '%d-%m-%Y %H:%M:%S')
        return redata
