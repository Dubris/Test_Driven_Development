from .base import TestFunctional
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time


class TestNewVisitor(TestFunctional):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.server_url)

        # She notices the page title and header mention to-do list
        assert 'To-Do' in self.browser.title
        header_text = self.browser.find_element_by_tag_name('h1').text
        assert 'To-Do' in header_text

        # She is invited to enter a to-do item straight away
        inputbox = self.get_item_input_box()
        assert inputbox.get_attribute('placeholder') == 'Enter a to-do item'

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, she is taken to a new URL, and now the page
        # lists "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(0.1)
        edith_list_url = self.browser.current_url
        assert '/lists/' in edith_list_url
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(0.1)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Now a new user, Francis, comes along to the site.

        # We use a new browser session to make sure that no information
        # of Edith's is coming through from cookies, etc.
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Francis vivits the homepage. There is no sign of Edith's list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        assert 'Buy peacock feathers' not in page_text
        assert 'make a fly' not in page_text

        # Francis starts a new list by entering a new item. He is less
        # interesting than Edith...
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(0.1)

        # Francis got his own unique URL
        francis_list_url = self.browser.current_url
        assert '/lists/' in francis_list_url
        assert francis_list_url != edith_list_url

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        assert 'Buy peacock feathers' not in page_text
        assert 'Buy milk' in page_text

        self.browser.quit()

        # Satisfied, they both go to sleep

        # Edith wonders whether the site will remember her list. Then
        # she sees that the site has generated a unique URL for her --
        # there is some explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep
