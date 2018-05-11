from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def check_for_item_in_list_table(self, item_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(item_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. she goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'), 'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into the text box (Edith's hobby
        # is tying fly-fishing lures)
        input_box.send_keys('Buy peacock feathers')

        # When she hit enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an items in a to-do list
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_item_in_list_table('1: Buy peacock feathers')

        # There is still a  text box inviting her to add another item. She
        # then enters "Use peacock feathers to make a fly" (Edith is very methodical)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys("Use peacock feathers to make a fly")
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now show both items on her list
        self.check_for_item_in_list_table('1: Buy peacock feathers')
        self.check_for_item_in_list_table('2: Use peacock feathers to make a fly')

        self.fail('Finish the test')

        # Edith wonders whether the site still remembers her lists. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text for that effect

        # She visits that URL -- her to-do lists is still there

        # Satisfied, she goes to bed
