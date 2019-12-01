import time
import socket

from django.test import LiveServerTestCase
from django.test import tag, override_settings
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException


MAX_WAIT = 20


@tag('selenium')
@override_settings(ALLOWED_HOSTS=['*'])
class SeleniumLiveServerTestCase(LiveServerTestCase):
    """
    Provides base test class which connects to the Docker
    container running selenium.
    """
    host = '0.0.0.0'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.host = socket.gethostbyname(socket.gethostname())
        cls.selenium = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.FIREFOX
        )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()



class NewVisitorTest(SeleniumLiveServerTestCase):

    def wait_for_welcome_message_after_entering_username(self, username):
        t_start = time.time()
        while True:
            try:
                welcome_msg = self.selenium.find_element_by_id('id_welcome_msg').text
                self.assertIn(username, welcome_msg)
                return
            except (AssertionError, NoSuchElementException) as e:
                if time.time() - t_start > MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def test_can_enter_a_username_and_retrieve_recommendations(self):
        # Manuel has heard about a cool new anime recommender system.
        # He goes to check out its homepage.
        self.selenium.get(self.live_server_url)

        # He notices the page title and header mention 'punpun.me' and
        # anime recommender systems.
        self.assertIn('punpun.me', self.selenium.title)
        header_text = self.selenium.find_element_by_tag_name('h1').text
        self.assertIn('punpun.me', header_text)
        subheader_text = self.selenium.find_element_by_tag_name('h2').text
        self.assertIn('a simple anime recommender system', subheader_text)

        # He is invited to enter his MyAnimeList username straight away.
        inputbox = self.selenium.find_element_by_id('id_enter_username')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter your MyAnimeList username'
        )

        # He enters his name: 'Manuel' and hits Enter. 
        inputbox.send_keys('Manuel')
        inputbox.send_keys(Keys.ENTER)

        # The page loads for some time and a welcome message is displayed.
        self.wait_for_welcome_message_after_entering_username('Manuel')

        # Also, a list of one hundred recommendations is displayed. 
        table = self.selenium.find_element_by_id('id_recs_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows), 100)

        # Satisfied he goes back to sleep.
