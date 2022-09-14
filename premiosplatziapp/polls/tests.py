import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(
            question_text="¿Quién es el mejor Course Director de Platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


#a good practices is create a function that creates a questions inside the tests
def create_question(question_text, days):
    """
    Create a question with the given question_text and published at the given numbers of days 
    offset to now (negative for questions in the past, positive for the ones in the future)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text = question_text, pub_date = time)


class QuestionIndexViewTests(QuestionModelTests, TestCase):

    def test_no_questions(self):
        """If no question exist, an appropiate message is displayed"""
        # * Hago una petición GET al index de polls y guardo la respuesta en response
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_questions_with_future_pub_date(self):
        """
        Questions with date greater to timezone.now shouldn't be displayed at index
        """
        create_question("Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])


    def test_questions_with_past_pub_date(self):
        """
        Questions with date in the past to timezone.now should be displayed at index
        """
        question = create_question("Past question", days=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question])