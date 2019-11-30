from django.shortcuts import render, redirect
from recommendations.models import Anime, User, Recommendation

import requests
import json


def get_if_exists(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:  # Be explicit about exceptions
        obj = None
    return obj


def home_page(request):
    if request.method == 'POST':
        new_username = request.POST['username']

        # Create new user if user doesn't exist.
        user = get_if_exists(User, name = new_username)
        if user is None:
            user = User.objects.create(name = new_username)

        response = requests.post(
            f'http://192.168.0.3:5000/predict?username={new_username}'
        )
        
        predictions = response.json()
        predictions = predictions['predictions']
        predictions = json.loads(predictions)

        for p in predictions:
            anime = get_if_exists(Anime, anime_id=p['anime_id'])
            if anime is None:
                anime = Anime.objects.create(anime_id = p['anime_id'])
            anime.title = p['title']
            anime.anime_type = p['type']
            anime.premiered = p['premiered']
            anime.genres = p['genre']
            anime.save()

            recommendation = get_if_exists(
                Recommendation, user = user, anime = anime
            )
            if recommendation is None:
                Recommendation.objects.create(
                    user=user,
                    anime=anime,
                    predicted_score = p['score']
                )
            else:
                recommendation.score = p['score']  # Update score.
                recommendation.save()

        # ToDo: Multiple SQL requests here! 
        recommendations = Recommendation.objects.filter(
            user__name = new_username
        )
        recommendations = recommendations.order_by('-predicted_score')

        return render(request, 'home.html', {
            'new_username': new_username,
            'recommendations': recommendations})

    else:
        return render(request, 'home.html')
