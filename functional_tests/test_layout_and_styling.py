from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):

    def test_home_page_layout_and_styling(self):

        # Edith has heard about a cool new flash card app called flippy. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the page title and header mentions Flippy
        self.assertIn('Flippy', self.browser.title)
        heading_text = self.browser.find_element(By.TAG_NAME, 'h1').text  
        self.assertIn('Flippy', heading_text)

        # and the subheading describes the site as a flashcards app
        subheading_text = self.browser.find_element(By.CLASS_NAME, 'lead').text  
        self.assertIn('Create, share, and learn from flashcards on any topic.', subheading_text)

        # There are a couple of call to action buttons
        button_list = self.browser.find_elements(By.CLASS_NAME, 'btn')

        #  The first button asks her to try out a random collection from all flashcards
        self.assertEqual(button_list[0].text, 'All flashcards from all decks')

        # And the second button asks her to try a random deck of flashcards
        self.assertEqual(button_list[1].text, 'All flashcards from a random deck')
