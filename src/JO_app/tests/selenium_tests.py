import time
from django.test import LiveServerTestCase
from selenium import webdriver

class InscriptionTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url)
        self.browser.implicitly_wait(10)  # Attendre jusqu'à 10 secondes pour que les éléments se chargent
        
    def tearDown(self):
        self.browser.quit()
    
    def test_inscription(self):
        # Remplir le formulaire d'inscription
        self.browser.find_element_by_css_selector('input[name="nom"]').send_keys('John')
        self.browser.find_element_by_css_selector('input[name="prenom"]').send_keys('Doe')
        self.browser.find_element_by_css_selector('input[name="email"]').send_keys('john@example.com')
        self.browser.find_element_by_css_selector('input[name="password1"]').send_keys('password123')
        self.browser.find_element_by_css_selector('input[name="password2"]').send_keys('password123')
        
        # Cliquer sur le bouton S'inscrire
        self.browser.find_element_by_css_selector('form button[type="submit"]').click()
        
        # Attendre un court moment pour que la page se recharge
        time.sleep(1)
        
        # Vérifier que l'utilisateur est redirigé vers la page de connexion
        self.assertIn('connexion', self.browser.current_url)
