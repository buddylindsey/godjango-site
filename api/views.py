from rest_framework.generics import CreateAPIView

from .serializers import SubscriberSerializer
from newsletter.tasks import newsletter_subscribe


class CreateSubscriber(CreateAPIView):
    serializer_class = SubscriberSerializer

    def perform_create(self, serializer):
        serializer.save()

        newsletter_subscribe.delay(
            serializer.validated_data['first_name'],
            serializer.validated_data['last_name'],
            serializer.validated_data['email'])
