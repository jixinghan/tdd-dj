from django.test import TestCase

from lists.views import home_page
from lists.models import Item

## view functions related tests ==============================================
class HomePageViewTest(TestCase):

    def test_use_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

class ListPageViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_all_items(self):
        # Assume we have a set of items
        item1 = Item.objects.create(text='item 1')
        item2 = Item.objects.create(text='item 2')
        # When client sends a request...
        response = self.client.get('/lists/the-only-list-in-the-world/')
        # all these items should be in the response
        self.assertContains(response, item1.text)
        self.assertContains(response, item2.text)

class CreateNewListViewTest(TestCase):

    def test_can_save_post_request_data_into_database(self):
        response = self.client.post(
            '/lists/create-new', data={'item_text': 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post_request(self):
        response = self.client.post(
            '/lists/create-new', data={'item_text': 'A new list item'}
        )
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

## model related tests =======================================================
class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

