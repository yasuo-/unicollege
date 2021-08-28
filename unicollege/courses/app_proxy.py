from django.utils import timezone

from ..core.models import BaseContentModel


class OrderedContentProxy(BaseContentModel):

    class Meta:
        proxy = True
        ordering = ['created_at']

    def created_delta(self):
        return timezone.now() - self.created_at
