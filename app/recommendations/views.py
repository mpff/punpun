from django.shortcuts import render, redirect
from recommendations.models import Anime, User, Recommendation

import requests


def home_page(request):
    if request.method == 'POST':
        new_username = request.POST['username']
        User.objects.create(name = new_username)

        response = requests.post(
            f'http://192.168.0.3:5000/predict?username={new_username}'
        )
        
        predictions = response.json()
        predictions = predictions['predictions']


        return redirect('/')

    recommendations = Recommendation.objects.all()

    return render(request, 'home.html', {'recommendations': recommendations})
