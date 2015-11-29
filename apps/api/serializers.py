from rest_framework.serializers import ModelSerializer, ValidationError

from episode.models import Video
from newsletter.models import Subscriber


class SubscriberSerializer(ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('first_name', 'last_name', 'email')

    def validate_email(self, value):
        """
        Verify not a duplicate subscriber.
        """
        if Subscriber.objects.filter(email=value, active=True).exists():
            raise ValidationError("You are already subscribed")
        return value


class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'pk', 'title', 'description', 'show_notes', 'video_h264',
            'video_webm', 'length', 'episode', 'publish_date', 'is_premium',
            'youtube_id'
        )
