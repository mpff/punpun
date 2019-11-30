from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from recommendations.models import Anime
from recommendations.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'username': 'Testuser'})
        self.assertIn('Testuser', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')


class AnimeModelTest(TestCase):

    def test_saving_and_retrieving_animes(self):
        first_anime = Anime()
        first_anime.title = "The best anime"
        first_anime.save()

        second_anime = Anime()
        second_anime.title = "The worst anime"
        second_anime.save()

        saved_animes = Anime.objects.all()
        self.assertEqual(saved_animes.count(), 2)

        first_saved_anime = saved_animes[0]
        second_saved_anime = saved_animes[1]

        self.assertEqual(first_saved_anime.title, "The best anime")
        self.assertEqual(second_saved_anime.title, "The worst anime")
