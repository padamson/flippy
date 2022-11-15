import os
from webbrowser import get
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from selenium import webdriver

#from selenium.webdriver.firefox.service import Service as FirefoxService
#from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

#from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.core.utils import ChromeType

from xvfbwrapper import Xvfb
import time
import platform
from django.contrib.auth import (
    SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
)
from django.test import RequestFactory
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings as django_settings

MAX_WAIT = 10

def on_staging_server():
    if os.environ.get('STAGING_SERVER'):
        return True
    else:
        return False

def wait(fn):  
    def modified_fn(*args, **kwargs):  
        start_time = time.time()
        while True:  
            try:
                return fn(*args, **kwargs)  
            except (AssertionError, WebDriverException) as e:  
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn  


class FunctionalTest(StaticLiveServerTestCase):  
    

    def quit_if_possible(self, browser):
        try: browser.quit()
        except: pass
        
    def create_pre_authenticated_session(self, user):
        '''Create an authenticated user quickly'''
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = django_settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()
        # visit domain (404 quickest)
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=django_settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
            secure=False,
            httpOnly=True
        ))


    def setUp(self):  
        if 'ubuntu' in platform.version().lower():
            self.xvfb = Xvfb(width=1280, height=720)
            self.addCleanup(self.xvfb.stop)
            self.xvfb.start()

        #self.browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        #self.browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'https://' + self.staging_server

    def tearDown(self):  
        self.browser.quit()

    @wait
    def wait_for_card_in_page(self, box_number, card_question):
        card_list = self.browser.find_elements(By.NAME, f'box_{box_number}_card')
        self.assertIn(card_question, [card.text for card in card_list])

    @wait
    def wait_for(self, fn):
        return fn()

    def get_question_input_box(self):
        return self.browser.find_element(By.NAME, 'question')

    def get_answer_input_box(self):
        return self.browser.find_element(By.NAME, 'answer')

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element(By.LINK_TEXT, 'Logout')
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(email, navbar.text)


    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element(By.LINK_TEXT, 'Login')
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertNotIn(email, navbar.text)
