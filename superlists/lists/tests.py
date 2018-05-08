from django.test import TestCase

from lists.views import home_page


class HomePageTest(TestCase):

    def test_use_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')
