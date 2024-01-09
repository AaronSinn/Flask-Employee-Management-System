import unittest
from selenium import webdriver
import page

class testCases(unittest.TestCase):

    test_first_name = 'test_first_name'
    test_last_name = 'test_last_name'
    test_username = 'test_username'
    test_password = 'test_password'

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://127.0.0.1:5000')

    #creates a new account
    def test_register_account(self):
        homePage = page.HomePage(self.driver)
        registerPage = page.RegisterPage(self.driver)
        dashboardPage = page.DashboardPage(self.driver)
        
        #checks we're on the home page
        assert homePage.is_title_matches(), 'Home page title does not match'
        homePage.click_register_link()
        
        #check we're on the register page
        assert registerPage.is_title_matches(), 'Register page title does not match'
        registerPage.first_name_element = self.test_first_name
        registerPage.last_name_element = self.test_last_name
        registerPage.username_element = self.test_username
        registerPage.password_element = self.test_password
        registerPage.click_submit()

        #checks we're on the dashboard after registering
        assert dashboardPage.is_title_matches(firstName=self.test_first_name, lastName=self.test_last_name), 'Dashboard title does not match'

    #attempts to create an account with a username already taken
    def test_register_duplicate_invalid(self):
        homePage = page.HomePage(self.driver)
        registerPage = page.RegisterPage(self.driver)
        
        #checks we're on the home page
        assert homePage.is_title_matches(), 'Home page title does not match'
        homePage.click_register_link()
        
        #check we're on the register page
        assert registerPage.is_title_matches(), 'Register page title does not match'
        registerPage.first_name_element = self.test_first_name
        registerPage.last_name_element = self.test_last_name
        registerPage.username_element = self.test_username
        registerPage.password_element = self.test_password
        registerPage.click_submit()

        #check we're on the register page
        assert registerPage.is_title_matches(), 'Not on the Register page after submiting a duplicate username'
        #checks if the message flash is displayed
        assert registerPage.is_account_duplicate(), 'Duplicate message flash not found'

    def test_login_account(self):
        homePage = page.HomePage(self.driver)
        loginPage = page.LoginPage(self.driver)
        dashboardPage = page.DashboardPage(self.driver)
        
        #checks we're on the home page
        assert homePage.is_title_matches(), 'Home page title does not match'
        homePage.click_login_link()

        #checks we're on the login page
        assert loginPage.is_title_matches(), 'Login page title does not match'
        #self.test_* cannot be used for this because the test account wont be in the database when this unit test runs
        loginPage.username_element = 'ALREADY_CREATED_USERNAME'
        loginPage.password_element = 'ALREADY_CREATED_PASSWORD'
        loginPage.click_submit()

        #checks that we're on the dashboard after logging in
        assert dashboardPage.is_title_matches(firstName='ALREADY_CREATED_FIRSTNAME', lastName='ALREADY_CREATED_LASTNAME'), 'Dashboard title does not match'
    
    def test_login_account_invalid(self):
        homePage = page.HomePage(self.driver)
        loginPage = page.LoginPage(self.driver)

        assert homePage.is_title_matches(), 'Home page title does not match'
        homePage.click_login_link()

        #checks we're on the login page
        assert loginPage.is_title_matches(), 'Login page title does not match'
        #self.test_* cannot be used for this because the test account wont be in the database when this unit test runs
        loginPage.username_element = 'INVALID_USERNAME'
        loginPage.password_element = 'INVALID_PASSWORD'
        loginPage.click_submit()

        #checks if the message flash is displayed
        assert loginPage.is_login_failed(), 'Login did not fail when a invalid username and password was passed'
        
        #checks that we're still on the login page
        assert loginPage.is_title_matches(), 'No longer on login page after invalid login attmept'

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()