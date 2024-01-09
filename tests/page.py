from locators import HomePageLocators, RegisterPageLocators, LoginPageLocators
from element import *

class BasePage():
    def __init__(self, driver):
        self.driver = driver
    
class HomePage(BasePage):

    #verifies the page title is the hard coded text
    def is_title_matches(self)-> bool:
        return 'Welcome to SquadSync' == self.driver.title
    
    def click_register_link(self):
        element = self.driver.find_element(*HomePageLocators.REGISTER_LINK)
        element.click()

    def click_login_link(self):
        element = self.driver.find_element(*HomePageLocators.LOGIN_LINK)
        element.click()

class RegisterPage(BasePage):

    first_name_element = RegisterFirstNameElements()
    last_name_element = RegisterLastNameElements()
    username_element = RegisterUsernameElements()
    password_element = RegisterPasswordElements()

    def is_title_matches(self)-> bool:
        return 'Register' == self.driver.title
    
    def click_submit(self):
        element = self.driver.find_element(*RegisterPageLocators.SUBMIT_BUTTON)
        element.click()

    def is_account_duplicate(self)-> bool:
        return "Username already taken." in self.driver.page_source 

class LoginPage(BasePage):
    username_element = LoginUsernameElements()
    password_element = LoginPasswordElements() 

    def is_title_matches(self)-> bool:
        return 'Login' == self.driver.title

    def is_login_failed(self)-> bool:
        return 'Username not found.' in self.driver.page_source 

    def click_submit(self):
        element = self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON)
        element.click()

class DashboardPage(BasePage):

    def is_title_matches(self, firstName, lastName)-> bool:
        print('PASSED:',f"{firstName} {lastName}'s Dashboard")
        print('ACTUAL:', self.driver.title)
        return f"{firstName} {lastName}'s Dashboard" == self.driver.title
    

    

