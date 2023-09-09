from django.db import models
from django.contrib.auth.models import AbstractUser

class Novel(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='novels')
    synopsis = models.TextField()
    author = models.CharField(max_length=100, default='Unknown')
    genre =  models.TextField(null='true')

    def __str__(self):
        return self.title

class Chapter(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    previous_chapter = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_chapters')
    next_chapter = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='previous_chapters')
    cart = models.ManyToManyField('novels.CustomUser', through='CartChapter')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=1.25)
    
    def __str__(self):
        return f"{self.novel.title} - {self.title}"
    
class CustomUser(AbstractUser):
    USER_ROLES = (
        (0, 'Admin'),
        (1, 'Customer'),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    user_id = models.IntegerField(choices=USER_ROLES, default=1)

    def __str__(self):
        return f'{self.username} (User ID: {self.user_id})'

class CartChapter(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('novels.CustomUser', on_delete=models.CASCADE, related_name='payments')
    chapter = models.ForeignKey('novels.Chapter', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment ID: {self.id}, User: {self.user.username}, Chapter: {self.chapter.title}"

