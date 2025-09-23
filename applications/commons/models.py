from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    content = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['pub_date']),
            models.Index(fields=['title', 'pub_date']),
            models.Index(fields=['-pub_date'], name='recent_articles_idx'),
        ]