from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create your tests here.

class LoginTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(LoginTestCase,self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(LoginTestCase, self).tearDown()

    def test_register(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/account/login')
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')

        submit=selenium.find_element_by_name('login')

        username.send_keys('ajay')
        password.send_keys('upakar123')

        #submitting the form
        submit.click()





