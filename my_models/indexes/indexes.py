from django.db import models
from django.db.models.functions import Lower
from django.db.models import F

class Article(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateField()
    height = models.FloatField()
    weight = models.FloatField()

    class Meta:
        indexes = [
            # Chỉ mục dùng hàm Lower và sắp giảm dần trên title, kết hợp pub_date
            models.Index(
                Lower('title').desc(),
                'pub_date',
                name='lower_title_date_idx'
            ),
            # Chỉ mục trên biểu thức nhân height * weight, và Round(weight)
            models.Index(
                F('height') * F('weight'),
                models.functions.Round('weight'),
                name='calc_idx'
            ),
        ]
