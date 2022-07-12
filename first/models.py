from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Store(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='title'
    )
    description = models.TextField(
        max_length=800,
        verbose_name='description'
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )

    def __str__(self):
        return self.title
