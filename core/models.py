from uuid import uuid4

from django.db import models


class WikiPage(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)

    title = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
