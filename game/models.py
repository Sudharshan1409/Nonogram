from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.


class Game(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='games')
    rows = models.IntegerField()
    columns = models.IntegerField()
    grid = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now, db_index=True, editable=False)
    updated_at = models.DateTimeField(blank=True, null=True, db_index=True, default=timezone.now)

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'

    def __str__(self):
        return self.name
