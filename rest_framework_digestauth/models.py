
from django.db import models


class DigestAuthCounter(models.Model):
    server_nonce = models.TextField()
    client_nonce = models.TextField()
    client_counter = models.IntegerField(null=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('server_nonce', 'client_nonce')
