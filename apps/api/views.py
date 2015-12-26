from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication
)

from rest_framework.viewsets import ModelViewSet

from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin
)

from .serializers import SubscriberSerializer, VideoSerializer
from newsletter.tasks import newsletter_subscribe
from episode.models import Video



class CreateSubscriber(CreateAPIView):
    serializer_class = SubscriberSerializer
    authentication_classes = (SessionAuthentication,)


    def perform_create(self, serializer):
        first_name = serializer.validated_data.get('first_name', '')
        last_name = serializer.validated_data.get('last_name', '')

        if serializer.validated_data['email']:
            newsletter_subscribe.delay(
                first_name, last_name, serializer.validated_data['email'],
                tags=['angular'])

        serializer.save()

class VideoViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
