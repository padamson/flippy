from selenium.webdriver.common.by import By
from .base import FunctionalTest
from cards.models import Card

class FlashcardPages(FunctionalTest):

    def test_all_flashcard_page(self):

        c1 = Card(question="Hello", answer="Hola")
        c1.save()
        c2 = Card(question="Please", answer="Por favor", box=2)
        c2.save()
        c3 = Card(question="Sorry", answer="Lo siento")
        c3.save()

        # Edith has heard about a cool new flash card app called flippy. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She sees a call to action button to try all of her flashcards
        all_cards_button = self.browser.find_element(By.ID, 'all_cards_button')

        # And she clicks it, taking her to a page showing all of the flashcards
        all_cards_button.click()
    
        # She notices that 'all' is in the url
        all_cards_url = self.browser.current_url
        self.assertRegex(all_cards_url, '/all/') 

        # She sees the only three cards on the site grouped by their box. Within each box,
        # flashcards are ordered by date created
        box_headings_in_order = ['🗃 1st Box', '🗃 2nd Box']
        box_footers_in_order = ['End 1st Box', 'End 2nd Box']
        card_questions_in_box_one_in_order = ['Sorry', 'Hello']
        card_questions_in_box_two_in_order = ['Please']
        for card_question in card_questions_in_box_one_in_order:
            self.wait_for_card_in_page(1, card_question)
        for card_question in card_questions_in_box_two_in_order:
            self.wait_for_card_in_page(2, card_question)
        box_one_card_list = self.browser.find_elements(By.NAME, 'box_1_card')
        self.assertEqual(len(box_one_card_list), 2)
        box_two_card_list = self.browser.find_elements(By.NAME, 'box_2_card')
        self.assertEqual(len(box_two_card_list), 1)
        for question, card_text in zip(card_questions_in_box_one_in_order,
                                       [card.text for card in box_one_card_list]):
            self.assertEqual(question, card_text)
        for question, card_text in zip(card_questions_in_box_two_in_order,
                                       [card.text for card in box_two_card_list]):
            self.assertEqual(question, card_text)
        box_headings_in_page = self.browser.find_elements(By.NAME, "box_heading")
        for box_heading, box_heading_text in zip(box_headings_in_order,
                                          [box_heading_in_page.text for box_heading_in_page in box_headings_in_page]):
            self.assertEqual(box_heading, box_heading_text)
        box_footers_in_page = self.browser.find_elements(By.NAME, "box_footer")
        for box_footer, box_footer_text in zip(box_footers_in_order,
                                          [box_footer_in_page.text for box_footer_in_page in box_footers_in_page]):
            self.assertEqual(box_footer, box_footer_text)
