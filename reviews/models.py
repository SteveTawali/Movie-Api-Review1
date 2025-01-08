from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.title
    
from django.contrib.auth.models import User

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user} for {self.movie}'