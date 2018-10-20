from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pytest
import time
import re


@pytest.fixture(scope="session")
def browser():
    browser = webdriver.Firefox()
    browser.implicitly_wait(2)
    yield browser
    browser.quit()


def check_for_row_in_list_table(browser, row_text):
    table = browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    assert row_text in [row.text for row in rows]


def test_layout_and_styling(browser, live_server):
    # Edith goes to the homepage
    browser.get(live_server.url)
    browser.set_window_size(1024, 768)
    
    #She notices the input box is nicely centered
    inputbox = browser.find_element_by_id('id_new_item')
    assert 512 == pytest.approx(
    inputbox.location['x'] + inputbox.size['width'] / 2, abs = 15
    )
    
    #She starts a new list and sees the input is nicely centered
    inputbox.send_keys('testing\n')
    inputbox = browser.find_element_by_id('id_new_item')
    assert 512 == pytest.approx(
    inputbox.location['x'] + inputbox.size['width'] / 2, abs = 15
    )
    

def test_can_start_a_list_and_retrieve_it_later(browser, live_server):
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    browser.get(live_server.url)

    # She notices the page title and header mention to-do list
    assert 'To-Do' in browser.title
    header_text = browser.find_element_by_tag_name('h1').text
    assert 'To-Do' in header_text

    # She is invited to enter a to-do item straight away
    inputbox = browser.find_element_by_id('id_new_item')
    assert inputbox.get_attribute('placeholder') == 'Enter a to-do item'

    # She types "Buy peacock feathers" into a text box (Edith's hobby
    # is tying fly-fishing lures)
    inputbox.send_keys('Buy peacock feathers')

    # When she hits enter, she is taken to a new URL, and now the page lists
    # "1: Buy peacock feathers" as an item in a to-do list
    inputbox.send_keys(Keys.ENTER)
    time.sleep(0.2)
    edith_list_url = browser.current_url
    assert '/lists/' in edith_list_url
    check_for_row_in_list_table(browser, '1: Buy peacock feathers')

    # There is still a text box inviting her to add another item. She
    # enters "Use peacock feathers to make a fly" (Edith is very methodical)
    inputbox = browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Use peacock feathers to make a fly')
    inputbox.send_keys(Keys.ENTER)
    time.sleep(2)
    
    # The page updates again, and now shows both items on her list
    check_for_row_in_list_table(browser, '1: Buy peacock feathers')
    check_for_row_in_list_table(browser, '2: Use peacock feathers to make a fly')

    # Now a new user, Francis, comes along to the site.
    
    ## We use a new browser session to make sure that no information
    ## of Edith's is coming through from cookies, etc.
    browser.quit()
    browser = webdriver.Firefox()
    
    # Francis vivits the homepage. There is no sign of Edith's list
    browser.get(live_server.url)
    page_text = browser.find_element_by_tag_name('body').text
    assert 'Buy peacock feathers' not in page_text
    assert 'make a fly' not in page_text
    
    # Francis starts a new list by entering a new item. He is less
    # interesting than Edith...
    inputbox = browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Buy milk')
    inputbox.send_keys(Keys.ENTER)
    time.sleep(2)

    # Francis got his own unique URL
    francis_list_url = browser.current_url
    assert '/lists/' in francis_list_url
    assert francis_list_url != edith_list_url
    
    # Again, there is no trace of Edith's list
    page_text = browser.find_element_by_tag_name('body').text
    assert 'Buy peacock feathers' not in page_text
    assert 'Buy milk' in page_text
    
    browser.quit()
    pytest.fail('Finish the test')
    
    # Satisfied, they both go to sleep
    
    # Edith wonders whether the site will remember her list. Then
    # she sees that the site has generated a unique URL for her --
    # there is some explanatory text to that effect.

    # She visits that URL - her to-do list is still there.

    # Satisfied, she goes back to sleep
