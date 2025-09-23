from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(TimeStampedModel):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = [['name', 'sku']]
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['price']),
        ]
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Các sản phẩm"

    def __str__(self):
        return f"{self.name} ({self.sku})"
