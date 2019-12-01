from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from recommendations.models import Anime, User, Recommendation
from recommendations.views import home_page
from recommendations.services import get_prediction

from unittest.mock import Mock, patch

import requests
import json


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Recommendation.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Anime.objects.count(), 0)


    @patch('recommendations.views.get_prediction')
    def test_can_save_a_POST_request(self, mock_get_prediction):
        anime = Anime.objects.create(anime_id=0, title="TestAnime")

        mock_json = {
            "prediction": [{"score": 8.00, "anime_id": 0}]
        }
        mock_get_prediction().json.return_value = mock_json
        
        response = self.client.post('/', data={'username': 'Testuser'})

        self.assertTrue(mock_get_prediction.called)
        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.first()
        self.assertEqual(new_user.name, 'Testuser')


    @patch('recommendations.views.get_prediction')
    def test_redirects_after_post(self, mock_get_prediction):
        anime = Anime.objects.create(anime_id=0, title="TestAnime")

        mock_json = {
            "prediction": [{"score": 8.00, "anime_id": 0}]
        }
        mock_get_prediction().json.return_value = mock_json

        response = self.client.post('/', data={'username': 'Testuser'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')


    @patch('recommendations.views.get_prediction')
    def test_displays_all_recommendations(self, mock_get_prediction):
        user = User.objects.create(name="Testuser")
        anime = Anime.objects.create(anime_id=0, title="TestAnime")
        anime1 = Anime.objects.create(anime_id=1,title="anime1")
        anime2 = Anime.objects.create(anime_id=2,title="anime2")

        mock_json = {
            "prediction": [{"score": 8.00, "anime_id": 0}]
        }
        mock_get_prediction().json.return_value = mock_json

        Recommendation.objects.create(user=user, anime=anime1, predicted_score=1.23)
        Recommendation.objects.create(user=user, anime=anime2, predicted_score=4.56)

        response = self.client.post('/', data={'username': 'Testuser'})
        
        self.assertIn('anime1', response.content.decode())
        self.assertIn('anime2', response.content.decode())


    @patch('recommendations.views.get_prediction')
    def test_can_save_duplicate_POST_request(self, mock_get_prediction):
        anime = Anime.objects.create(anime_id=0, title="TestAnime")
        mock_json = {
            "prediction": [{"score": 8.00, "anime_id": 0}]
        }
        mock_get_prediction().json.return_value = mock_json

        response = self.client.post('/', data={'username': 'Testuser'})
        self.assertEqual(User.objects.count(), 1)
        response = self.client.post('/', data={'username': 'Testuser'})
        self.assertEqual(User.objects.count(), 1)



class ServiceTest(TestCase):

    @patch('recommendations.services.requests.post')
    def test_can_access_api(self, mock_post):
        mock_post.return_value.ok = True
        response = get_prediction('Manuel')
        self.assertIsNotNone(response.ok)


    @patch('recommendations.services.requests.post')
    def test_api_returns_prediction_as_json_when_response_is_ok(self, mock_post):
        json_response = {
            "prediction": [{"score": 9.878677508, "anime_id": 440}]
        }
        
        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.json.return_value = json_response

        response = get_prediction('Testuser')

        self.assertEqual(response.json(), json_response)


    @patch('recommendations.services.requests.post')
    def test_api_returns_none_when_response_is_not_ok(self, mock_post):
        mock_post.return_value.ok = False
        response = get_prediction('Testuser')
        self.assertIsNone(response)




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

