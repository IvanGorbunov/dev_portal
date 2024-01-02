from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse_lazy
from django.test import override_settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@override_settings(ALLOWED_HOSTS=['*'])  # Disable ALLOW_HOSTS
class TestProjectListPage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def tearDown(self):
        self.browser.quit()

    def test_on_logo(self):
        self.browser.get(self.live_server_url)

        alert = self.browser.find_elements(By.CLASS_NAME, 'logo-font')
        self.assertEqual(len(alert), 2)
        self.assertEqual(alert[0].text, 'Ivan')
        self.assertEqual(alert[1].text, 'Tech')
