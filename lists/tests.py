from django.test import TestCase

from lists.views import home_page
from lists.models import Item, List

## related with 'home_page' func view
class HomePageViewTest(TestCase):

    def test_use_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

## related with 'list_page' func view
class ListPageViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_only_items_for_the_specific_list(self):
        # Assume we have several items associated to a list
        list_ = List.objects.create()
        item1 = Item.objects.create(text='item 1', list=list_)
        item2 = Item.objects.create(text='item 2', list=list_)
        # Assume we have several items associated to another list
        another_list = List.objects.create()
        another_item1 = Item.objects.create(text='another 1', list=another_list)
        another_item2 = Item.objects.create(text='another 2', list=another_list)
        # When sends a request for a specific list
        response = self.client.get(f'/lists/{list_.id}/')
        # all the items associated with that list should be in the response
        self.assertContains(response, item1.text)
        self.assertContains(response, item2.text)
        self.assertNotContains(response, another_item1.text)
        self.assertNotContains(response, another_item2.text)

    def test_pass_correct_list_to_template(self):
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

## related with 'create_new_list' func view
class NewListViewTest(TestCase):

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
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

## related with 'add_item' func view
class NewItemViewTest(TestCase):
    
    def test_can_save_a_item_in_a_post_reqeust_to_a_correct_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add-item',
            data = {'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_a_correct_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add-item',
            data = {'item_text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)
