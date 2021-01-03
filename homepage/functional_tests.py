from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import unittest


class NewTest(unittest.TestCase):

    def setUp(self):
        self.options = Options()
        self.browser = webdriver.Firefox(options=self.options,
                                         executable_path=r'C:\Users\gora-pc\AppData\Local\Programs\Python\Python38-32\Scripts\geckodriver.exe')
        # self.options.headless = True

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_site_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Olaawa', self.browser.title)
        self.fail('Zakończenie testu')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
