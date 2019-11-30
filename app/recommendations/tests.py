from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from recommendations.models import Anime, User, Recommendation
from recommendations.views import home_page

import requests


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Anime.objects.count(), 0)


    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'username': 'Testuser'})
        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.first()
        self.assertEqual(new_user.name, 'Testuser')


    def test_redirects_after_post(self):
        response = self.client.post('/', data={'username': 'Testuser'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')


    def test_displays_all_recommendations(self):
        user = User.objects.create(name="Testuser")
        anime1 = Anime.objects.create(anime_id=0,title="anime1")
        anime2 = Anime.objects.create(anime_id=1,title="anime2")

        Recommendation.objects.create(user=user, anime=anime1, predicted_score=1.23)
        Recommendation.objects.create(user=user, anime=anime2, predicted_score=4.56)

        response = self.client.get('/')
        
        self.assertIn('anime1', response.content.decode())
        self.assertIn('anime2', response.content.decode())



class ApiTest(TestCase):

    def test_can_access_REST_api(self):
        new_username = 'Manuel'
        response = requests.post(
            f'http://192.168.0.3:5000/predict?username={new_username}'
        )
        self.assertTrue(response.ok)


class ModelTest(TestCase):

    def test_saving_and_retrieving_animes(self):
        first_anime = Anime()
        first_anime.anime_id = 1
        first_anime.title = "The best anime"
        first_anime.save()

        second_anime = Anime()
        second_anime.anime_id = 2
        second_anime.title = "The worst anime"
        second_anime.save()

        saved_animes = Anime.objects.all()
        self.assertEqual(saved_animes.count(), 2)

        first_saved_anime = saved_animes[0]
        second_saved_anime = saved_animes[1]

        self.assertEqual(first_saved_anime.title, "The best anime")
        self.assertEqual(second_saved_anime.title, "The worst anime")


    def test_saving_and_retrieving_users(self):
        user1 = User()
        user1.name = "User1"
        user1.save()

        user2 = User()
        user2.name = "User2"
        user2.save()

        saved_users = User.objects.all()
        self.assertEqual(saved_users.count(), 2)

        first_saved_user = saved_users[0]
        second_saved_user = saved_users[1]

        self.assertEqual(first_saved_user.name, "User1")
        self.assertEqual(second_saved_user.name, "User2")


    def test_saving_and_retrieving_recommendations(self):
        user = User()
        user.name = "Testa"
        user.save()

        anime = Anime()
        anime.anime_id = 1
        anime.anime_title = "Bebopo"
        anime.save()

        recommendation = Recommendation()
        recommendation.user = user
        recommendation.anime = anime
        recommendation.predicted_score = 1.23
        recommendation.save()

