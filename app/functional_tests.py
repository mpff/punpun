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

        table = self.browser.find_element_by_id('id_recs_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == 'Revolutionary Girl Utena' for row in rows),
            "Recommendation did not appear in table"
        )

        # There is still a text box inviting her to add another item. She
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main()
