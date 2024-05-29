
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import unittest
import time

class InscriptionTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.get('http://localhost:8000/JO_app/inscription')

    def tearDown(self):
        self.browser.quit()

    def test_inscription(self):
        wait = WebDriverWait(self.browser, 10)
        
        nom_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="nom"]')))
        nom_input.send_keys('John')

        prenom_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="prenom"]')))
        prenom_input.send_keys('Doe')

        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="email"]')))
        email_input.send_keys('johndoe@example.com')

        password1_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password1"]')))
        password1_input.send_keys('password1234567')

        password2_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password2"]')))
        password2_input.send_keys('password1234567')

        self.browser.save_screenshot('before_submit.png')

        submit_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
        submit_button.click()

        time.sleep(2)
        
        self.browser.save_screenshot('after_submit.png')

        try:
            success_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.success')))
            self.assertIn('Inscription réussie', success_message.text)
        except TimeoutException:
            self.browser.save_screenshot('error.png')
            raise

if __name__ == '__main__':
    unittest.main()
