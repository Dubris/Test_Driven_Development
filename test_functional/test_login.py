from selenium.webdriver.support.ui import WebDriverWait
from .base import TestFunctional
import time


class LoginTest(TestFunctional):

    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return
                retries -= 1
                time.sleep(0.5)
            self.fail('Could not find the window')

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id)
        )

    def test_login_with_auth0(self):
        # Edith goes to the site
        # and notices a "Sign in" link for the first time
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('btn-login').click()

        # An auth0 login box appears
        self.switch_to_new_window('Sign In with Auth0')

        # Edith logs in with Google account
        # Use mockmyid.com for test email
        time.sleep(3)
        self.browser.find_element_by_name('email'
                                          ).send_keys('testswebappli@gmail.com')
        self.browser.find_element_by_name('password'
                                          ).send_keys('Test123!!\n')

        # The auth0 windows closes
        time.sleep(1)
        try:
            self.switch_to_new_window('Authorize Application')
            self.browser.find_element_by_id('allow').click()
        except AssertionError:
            pass

        self.switch_to_new_window('To-Do lists')

        # She can see that she is logged in
        self.wait_for_element_with_id('btn-logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        assert 'testswebappli@gmail.com' in navbar.text
