from django.db import models

class Anime(models.Model):
    anime_id = models.IntegerField(default=0, primary_key=True)
    title = models.TextField(default='')
    anime_type = models.TextField(blank=True)
    genres = models.TextField(blank=True)
    premiered = models.TextField(blank=True)


class User(models.Model):
    name = models.TextField(default='', unique=True)


class Recommendation(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    anime = models.ForeignKey('Anime', on_delete=models.CASCADE)
    predicted_score = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        unique_together = ('user', 'anime')
