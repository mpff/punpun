import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention punpun 
        self.assertIn('punpun.me', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('punpun.me', header_text)
        subheader_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('a simple anime recommender system', subheader_text)

        # She is invited to enter her mal username straight away
        inputbox = self.browser.find_element_by_id('id_enter_username')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter your MyAnimeList username'
        )

        # She enters 'Manuel' right away
        inputbox.send_keys('Manuel')

        # When she hits enter, the page updates 
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # A welcome message is displayed.
        welcome_msg = self.browser.find_element_by_id('id_welcome_msg').text
        self.assertIn('Manuel', welcome_msg)

        # A list of one hundred recommendations is displayed. 
        table = self.browser.find_element_by_id('id_recs_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows), 100)

        # The first recommendation is Revolutionary Girl Utena.
        self.assertTrue(
            any(row.text == 'Revolutionary Girl Utena' for row in rows),
            f"Recommendations did not appear in table. Contents were:\n{table.text}"
        )

        # Satisfied he goes back to sleep.


if __name__ == '__main__':
    unittest.main()
