from django.core.management.base import BaseCommand, CommandError
from recommendations.models import Anime

import pickle
import pandas

class Command(BaseCommand):
    help = "Migrates anime meta data."
    
    def handle(self, *args, **options):
        # Load Kaggle dataset and populate database with animes.
        path = "recommendations/migrations/meta.pickle"
        with open(path, "rb") as f:
            meta = pickle.load(f)

        for i,anime in meta.iterrows():
            obj = Anime.objects.create(anime_id = anime.anime_id)
            obj.title = anime.title
            obj.anime_type = anime.type
            obj.genres = anime.genre
            obj.premiered = anime.premiered
            obj.save()
        
