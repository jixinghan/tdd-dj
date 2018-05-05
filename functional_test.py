from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.broswer = webdriver.Chrome()

    def tearDown(self):
        self.broswer.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. she goes
        # to check out its homepage
        self.broswer.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.broswer.title)
        self.fail('Finish the test!')

        # She is invited to enter a to-do item straight away

        # She types "Buy peacock feathers" into the text box (Edith's hobby
        # is tying fly-fishing lures)

        # When she his enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an items in a to-do list

        # There is still a  text box inviting her to add another item. She
        # then enters "Use peacock feathers to make a fly" (Edith is very methodical)

        # The page updates again, and now show both items on her list

        # Edith wonders whether the site still remembers her lists. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text for that effect

        # She visits that URL -- her to-do lists is still there

        # Satisfied, she goes to bed

if __name__ == '__main__':
    unittest.main(warnings='ignore')
