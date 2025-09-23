from django.db import models

class HomaUser(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class HomaProfile(HomaUser):
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Homa Profile"
        verbose_name_plural = "Homa Profiles"
        db_table = 'homa_profiles'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
        ]
        permissions = [
            ('can_view_profiles', 'Can view profiles'),
            ('can_edit_profiles', 'Can edit profiles'),
        ]

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        # Tên hiển thị
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Các sản phẩm"

        # Tên bảng tùy chỉnh
        db_table = 'shop_products'

        # Sắp xếp mặc định
        ordering = ['-created_at', 'name']

        # Index để tăng tốc truy vấn
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['name']),
        ]

        # Ràng buộc duy nhất
        unique_together = ['name', 'category']

        # Quyền tùy chỉnh
        permissions = [
            ('can_manage_inventory', 'Có thể quản lý kho'),
            ('can_set_prices', 'Có thể đặt giá'),
        ]

        # Ràng buộc kiểm tra
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gt=0),
                name='positive_price'
            ),
        ]