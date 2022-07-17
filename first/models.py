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
    owner = models.ForeignKey(
        'auth.User',
        related_name='stores',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.CharField(
        choices=(
            ('active', 'Active'),
            ('deactivated', 'Deactivated'),
            ('in_review', 'In_review')
        ),
        max_length=25,
        default='in_review'
    )

    def __str__(self):
        return self.title
