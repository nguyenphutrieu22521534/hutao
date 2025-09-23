from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Họ và tên")
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Tác giả"
        verbose_name_plural = "Các tác giả"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_date']  # mới nhất trước
        db_table = 'blog_posts'
        get_latest_by = 'published_date'

    def __str__(self):
        return self.title
