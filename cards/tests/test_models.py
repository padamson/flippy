from cards.models import Card
from django.test import TestCase

class TestCardModel(TestCase):

    def test_card_attributes(self):

        c1 = Card(question="Hello", answer="Hola")
        c1.save()
        c2 = Card(question="Please", answer="Por favor")
        c2.save()
        c3 = Card(question="Sorry", answer="Lo siento", box=2)
        c3.save()

        self.assertEqual(len(Card.objects.all()), 3)
        self.assertEqual(['Hello', 'Please', 'Sorry'],
                         [card.question for card in Card.objects.all()])
        self.assertEqual(['Hola', 'Por favor', 'Lo siento'],
                         [card.answer for card in Card.objects.all()])
        self.assertEqual([1, 1, 2], 
                         [card.box for card in Card.objects.all()])
                      
