from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse_lazy
from django.test import override_settings
from selenium import webdriver
from selenium.webdriver.common.by import By


@override_settings(ALLOWED_HOSTS=['*'])  # Disable ALLOW_HOSTS
class TestProjectListPage(StaticLiveServerTestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(executable_path='./functional_tests/chromedriver', chrome_options=chrome_options)
        print(f'\nchromedriverVersion: {self.browser.capabilities["chrome"]["chromedriverVersion"]}\n')

    def tearDown(self):
        self.browser.quit()

    def test_on_logo(self):
        self.browser.get(self.live_server_url + '/clients/answer/')

        alert = self.browser.find_elements(By.CLASS_NAME, 'logo-font')
        self.assertEqual(len(alert), 2)
        self.assertEquals(alert[0].text, 'Ivan')
        self.assertEquals(alert[1].text, 'Tech')

    def test_main_text(self):
        self.browser.get(self.live_server_url + '/clients/answer/')

        alert = self.browser.find_element(By.CLASS_NAME, 'col-md-6')
        self.assertEquals(alert.find_element(By.TAG_NAME, 'h4').text, 'Ваша заявка будет обработана в ближайшее время и параметры авторизации придут на электронную почту.')
