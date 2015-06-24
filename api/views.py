from rest_framework.generics import CreateAPIView

from .serializers import SubscriberSerializer
from newsletter.tasks import newsletter_subscribe


class CreateSubscriber(CreateAPIView):
    serializer_class = SubscriberSerializer

    def perform_create(self, serializer):
        serializer.save()

        first_name = serializer.validated_data.get('first_name', '')
        last_name = serializer.validated_data.get('last_name', '')

        if serializer.validated_data['email']:
            newsletter_subscribe.delay(
                first_name, last_name, serializer.validated_data['email'])
