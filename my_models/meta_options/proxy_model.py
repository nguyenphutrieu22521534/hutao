from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publish_date = models.DateField()

    class Meta:
        ordering = ['title']
        verbose_name = "Sách"
        verbose_name_plural = "Các cuốn sách"

    def __str__(self):
        return self.title

class BookProxy(Book):
    class Meta:
        proxy = True
        ordering = ['-publish_date']
        verbose_name = "Sách (Theo thời gian)"
        verbose_name_plural = "Danh sách sách theo thời gian"

    def recent(self):
        """Trả về bản ghi mới nhất theo publish_date"""
        return BookProxy.objects.first()

class LibraryMember(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    member_since = models.DateField()

    class Meta:
        permissions = [
            ("can_borrow", "Can borrow books"),
            ("can_view_member_details", "Can view member details"),
        ]
        verbose_name = "Thành viên thư viện"
        verbose_name_plural = "Các thành viên thư viện"

    def __str__(self):
        return self.user.username
