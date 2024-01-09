from selenium.webdriver.common.by import By

class HomePageLocators():
    REGISTER_LINK = (By.ID, 'regLink')
    LOGIN_LINK = (By.ID, 'loginLink')

class RegisterPageLocators():
    SUBMIT_BUTTON = (By.ID, 'submit')

class LoginPageLocators():
    LOGIN_BUTTON = (By.ID, 'submit')
