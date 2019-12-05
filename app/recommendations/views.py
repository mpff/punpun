from django.shortcuts import render, redirect
from recommendations.models import Anime, User, Recommendation
from recommendations.services import get_prediction

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

        # Get prediction from API
        response = get_prediction(new_username)

        # Format JSON to list.
        # TODO: Clean up json response of API.
        prediction = response.json()
        prediction = prediction['prediction']

        # Sort by score
        prediction = sorted(prediction, key=lambda k: k['score'], reverse=True)

        # Create object for each recommendation.
        # TODO: Filter this somehow better! 
        for p in prediction[:100]:
            anime = Anime.objects.get(anime_id=p['anime_id'])
            recommendation = get_if_exists(Recommendation, user = user, anime = anime)
            if recommendation is None:
                Recommendation.objects.create(
                    user=user,
                    anime=anime,
                    predicted_score = p['score']
                )
            else:
                recommendation.score = p['score']  # Update score.
                recommendation.save()

        # Filter for current user.
        # ToDo: Multiple SQL requests here! 
        recommendations = Recommendation.objects.filter(user__name = new_username)
        recommendations = recommendations.order_by('-predicted_score')[:100]

        return render(request, 'home.html', {
            'new_username': new_username,
            'recommendations': recommendations
        })

    
    return render(request, 'home.html')
