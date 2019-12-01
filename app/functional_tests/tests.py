import time
import socket

from django.test import LiveServerTestCase
from django.test import tag, override_settings

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


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
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()



class NewVisitorTest(SeleniumLiveServerTestCase):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.selenium.get(self.live_server_url)

        # She notices the page title and header mention punpun 
        self.assertIn('punpun.me', self.selenium.title)
        header_text = self.selenium.find_element_by_tag_name('h1').text
        self.assertIn('punpun.me', header_text)
        subheader_text = self.selenium.find_element_by_tag_name('h2').text
        self.assertIn('a simple anime recommender system', subheader_text)

        # She is invited to enter her mal username straight away
        inputbox = self.selenium.find_element_by_id('id_enter_username')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter your MyAnimeList username'
        )

        # She enters 'Manuel' right away
        inputbox.send_keys('Manuel')

        # When she hits enter, the page updates 
        inputbox.send_keys(Keys.ENTER)
        time.sleep(5)

        # A welcome message is displayed.
        welcome_msg = self.selenium.find_element_by_id('id_welcome_msg').text
        self.assertIn('Manuel', welcome_msg)

        # A list of one hundred recommendations is displayed. 
        table = self.selenium.find_element_by_id('id_recs_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows), 100)

        # Satisfied he goes back to sleep.
