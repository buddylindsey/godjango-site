from django.db import models

class Subscription(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    plan = models.CharField(max_length=50)

    def __unicode__(self):
        return self.title
