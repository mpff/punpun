from django.db import models

class Anime(models.Model):
    title = models.TextField(default='')
