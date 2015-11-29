from django.db import models

from django_extensions.db.fields.json import JSONField


class Subscriber(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=75)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.email


class Event(models.Model):
    kind = models.CharField(max_length=50)
    data = JSONField()

    def __unicode__(self):
        return self.kind

    def process(self):
        email = self.data.get('data[email]', None)
        first_name = self.data.get('data[merges][FNAME]', None)
        last_name = self.data.get('data[merges][LNAME]', None)
        old_email = self.data.get('data[old_email]', None)
        new_email = self.data.get('data[new_email]', None)

        if self.kind == 'subscribe':
            sub = Subscriber.objects.filter(email=email)
            if sub.exists():
                s = sub.get()
                s.active = True
                s.first_name = first_name
                s.last_name = last_name
                s.save()
            else:
                Subscriber.objects.create(
                    email=email, first_name=first_name, last_name=last_name,
                    active=True)

        elif self.kind == 'unsubscribe':
            try:
                sub = Subscriber.objects.get(email=email)
                sub.active = False
                sub.save(update_fields=['active'])
            except Subscriber.DoesNotExist:
                pass

        elif self.kind == 'profile':
            try:
                sub = Subscriber.objects.get(email=email)
                sub.first_name = first_name
                sub.last_name = last_name
                sub.save(update_fields=['first_name', 'last_name'])
            except Subscriber.DoesNotExist:
                pass

        elif self.kind == 'upemail':
            try:
                sub = Subscriber.objects.get(email=old_email)
                sub.email = new_email
                sub.save(update_fields=['email'])
            except Subscriber.DoesNotExist:
                pass
