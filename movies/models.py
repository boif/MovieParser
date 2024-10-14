from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    director = models.CharField(max_length=255)
    imdb_rating = models.FloatField()
    description = models.TextField()
    poster = models.ImageField(upload_to = 'movies/posters/', null = True, blank = True)

    def __str__(self):
        return self.title
