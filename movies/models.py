from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    director = models.CharField(max_length=255)
    imdb_rating = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.title
