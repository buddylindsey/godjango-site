from rest_framework.generics import CreateAPIView

from .serializers import SubscriberSerializer

class CreateSubscriber(CreateAPIView):
    serializer_class = SubscriberSerializer
