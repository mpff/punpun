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
        json = response.json()
        prediction = json['prediction']
        animelist = json['animelist']

        # Filter and sort predictions.      
        watched = [a['anime_id'] for a in animelist if a['status'] in [1,2,3,4]]
        recommendation = [p for p in prediction if p['anime_id'] not in watched]
        recommendation = sorted(recommendation, key=lambda k: k['score'], reverse=True)[:100]


        # Create object for each recommendation.
        # TODO: Filter this somehow better! 
        for i,r in enumerate(recommendation):
            anime = Anime.objects.get(anime_id=r['anime_id'])
            recommendation[i]['anime'] = anime


        return render(request, 'home.html', {
            'new_username': new_username,
            'animelist': animelist,
            'prediction': prediction,
            'recommendation': recommendation
        })

    
    return render(request, 'home.html')
