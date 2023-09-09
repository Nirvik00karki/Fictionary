from django.db import models

# Create your models here.

class ProductReview(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    review_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
