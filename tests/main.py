import unittest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import page
import time

class testCases(unittest.TestCase):

    test_first_name = 'test_first_name'
    test_last_name = 'test_last_name'
    test_username = 'test_username'
    test_password = 'test_password'

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", False) #close brower after execution
        options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('http://127.0.0.1:5000')

    #creates a new account
    def test_register_account(self):
        homePage = page.HomePage(self.driver)
        registerPage = page.RegisterPage(self.driver)
        dashboardPage = page.DashboardPage(self.driver)
        
        #checks we're on the home page
        self.driver.implicitly_wait(3)
        assert homePage.is_title_matches(), 'Home page title does not match'
        homePage.click_register_link()
        
        #check we're on the register page
        self.driver.implicitly_wait(3)
        assert registerPage.is_title_matches(), 'Register page title does not match'
        registerPage.first_name_element = self.test_first_name
        registerPage.last_name_element = self.test_last_name
        registerPage.username_element = self.test_username
        registerPage.password_element = self.test_password
        registerPage.click_submit()
        
        #checks we're on the dashboard after registering
        WebDriverWait(self.driver, 100).until(
            lambda driver: driver.find_element(By.CLASS_NAME,'summary-box'))
        assert dashboardPage.is_title_matches(firstName=self.test_first_name, lastName=self.test_last_name), 'Dashboard title does not match'

    #attempts to create an account with a username already taken
    def test_register_duplicate_invalid(self):
        homePage = page.HomePage(self.driver)
        registerPage = page.RegisterPage(self.driver)
        
        #checks we're on the home page
        self.driver.implicitly_wait(3)
        assert homePage.is_title_matches(), 'Home page title does not match'
        homePage.click_register_link()
        
        #check we're on the register page
        self.driver.implicitly_wait(3)
        assert registerPage.is_title_matches(), 'Register page title does not match'
        registerPage.first_name_element = self.test_first_name
        registerPage.last_name_element = self.test_last_name
        registerPage.username_element = self.test_username
        registerPage.password_element = self.test_password
        registerPage.click_submit()

        #check we're on the register page
        self.driver.implicitly_wait(3)
        assert registerPage.is_title_matches(), 'Not on the Register page after submiting a duplicate username'
        #checks if the message flash is displayed
        self.driver.implicitly_wait(3)
        assert registerPage.is_account_duplicate(), 'Duplicate message flash not found'

    def test_login_account(self):
        homePage = page.HomePage(self.driver)
        loginPage = page.LoginPage(self.driver)
        dashboardPage = page.DashboardPage(self.driver)
        
        #checks we're on the home page
        self.driver.implicitly_wait(3)
        assert homePage.is_title_matches(), 'Home page title does not match'
        homePage.click_login_link()

        #checks we're on the login page
        self.driver.implicitly_wait(3)
        assert loginPage.is_title_matches(), 'Login page title does not match'
        #self.test_* cannot be used for this because the test account wont be in the database when this unit test runs
        loginPage.username_element = 'ALREADY_CREATED_USERNAME'
        loginPage.password_element = 'ALREADY_CREATED_PASSWORD'
        loginPage.click_submit()

        #checks that we're on the dashboard after logging in
        WebDriverWait(self.driver, 100).until(
            lambda driver: driver.find_element(By.CLASS_NAME,'summary-box'))
        assert dashboardPage.is_title_matches(firstName='ALREADY_CREATED_FIRSTNAME', lastName='ALREADY_CREATED_LASTNAME'), 'Dashboard title does not match'
        return True
    
    def test_login_account_invalid(self):
        homePage = page.HomePage(self.driver)
        loginPage = page.LoginPage(self.driver)

        self.driver.implicitly_wait(3)
        assert homePage.is_title_matches(), 'Home page title does not match'
        homePage.click_login_link()

        #checks we're on the login page
        self.driver.implicitly_wait(3)
        assert loginPage.is_title_matches(), 'Login page title does not match'

        #self.test_* cannot be used for this because the test account wont be in the database when this unit test runs
        loginPage.username_element = 'INVALID_USERNAME'
        loginPage.password_element = 'INVALID_PASSWORD'
        loginPage.click_submit()

        #checks if the message flash is displayed
        self.driver.implicitly_wait(3)
        assert loginPage.is_login_failed(), 'Login did not fail when a invalid username and password was passed'
        
        #checks that we're still on the login page
        self.driver.implicitly_wait(3)
        assert loginPage.is_title_matches(), 'No longer on login page after invalid login attmept'

    def test_position(self):
        dashboardPage = page.DashboardPage(self.driver)
        positionPage = page.PositionPage(self.driver)

        assert self.test_login_account()

        self.driver.implicitly_wait(3)
        assert dashboardPage.is_title_matches(firstName='ALREADY_CREATED_FIRSTNAME', lastName='ALREADY_CREATED_LASTNAME'), 'Dashboard title does not match'
        
        dashboardPage.click_positions_link()
        #checks we're on the Position page
        self.driver.implicitly_wait(3)
        assert positionPage.is_title_matches(), 'Position page title does not match'

        positionPage.title_element = 'test_position_title'
        positionPage.description_element = 'test_position_description'
        positionPage.base_pay_elements = '123456'
        positionPage.click_submit()

        self.driver.implicitly_wait(3)
        assert positionPage.is_any_position_found(), 'Position was not added correctly'

    def test_position_invalid(self):
        dashboardPage = page.DashboardPage(self.driver)
        positionPage = page.PositionPage(self.driver)

        self.test_login_account()

        self.driver.implicitly_wait(3)
        assert dashboardPage.is_title_matches(firstName='ALREADY_CREATED_FIRSTNAME', lastName='ALREADY_CREATED_LASTNAME'), 'Dashboard title does not match'
        
        dashboardPage.click_positions_link()
        #checks we're on the Position page
        self.driver.implicitly_wait(3)
        assert positionPage.is_title_matches(), 'Position page title does not match'

        position_count_before = positionPage.get_position_count()

        positionPage.title_element = 'ALREADY_CREATED_TITLE'
        positionPage.description_element = 'ALREADY_CREATED_DESCRIPTION'
        positionPage.base_pay_elements = '123456'
        ActionChains(self.driver).move_to_element(self.driver.find_element(By.ID, 'submit')).perform()
        positionPage.click_submit()

        self.driver.implicitly_wait(3)

        position_count_after= positionPage.get_position_count()

        #the before and after count should be equal because a position that already exists cannot be added
        assert position_count_before == position_count_after, 'Position that arleady exists has been added'
    
    def test_department(self):
        dashboardPage = page.DashboardPage(self.driver)
        departmentsPage = page.DepartmentPage(self.driver)

        assert self.test_login_account()
        self.driver.implicitly_wait(3)
        assert dashboardPage.is_title_matches(firstName='ALREADY_CREATED_FIRSTNAME', lastName='ALREADY_CREATED_LASTNAME'), 'Dashboard title does not match'

        dashboardPage.click_departments_link()

        self.driver.implicitly_wait(3)
        assert departmentsPage.is_title_matches()

        departmentsPage.title_element='test_department_title'
        departmentsPage.description_element='test_department_description'
        departmentsPage.click_submit()

        assert departmentsPage.is_any_departments_found(), 'Department was not created correctly'

    def test_department_invalid(self):
        dashboardPage = page.DashboardPage(self.driver)
        departmentsPage = page.DepartmentPage(self.driver)

        assert self.test_login_account()
        self.driver.implicitly_wait(3)
        assert dashboardPage.is_title_matches(firstName='ALREADY_CREATED_FIRSTNAME', lastName='ALREADY_CREATED_LASTNAME'), 'Dashboard title does not match'

        dashboardPage.click_departments_link()

        self.driver.implicitly_wait(3)
        assert departmentsPage.is_title_matches()

        department_count_before = departmentsPage.get_department_count()

        departmentsPage.title_element='ALREADY_CREATED_DEPARTMENT_TITLE'
        departmentsPage.description_element='ALREADY_CREATED_DEPARTMENT_DESCRIPTION'
        departmentsPage.click_submit()

        self.driver.implicitly_wait(3)
        department_count_after = departmentsPage.get_department_count()

        assert department_count_before == department_count_after, 'Department that already exists was created'

        def test_employees(self):
            dashboardPage = page.DashboardPage(self.driver)
            employeesPage = page.EmployeePage(self.driver)

            assert self.test_login_account()
            self.driver.implicitly_wait(3)
            assert dashboardPage.is_title_matches(firstName='ALREADY_CREATED_FIRSTNAME', lastName='ALREADY_CREATED_LASTNAME'), 'Dashboard title does not match'

            dashboardPage.click_employes_link()

            employeesPage.first_name_element = 'test_first_name'
            employeesPage.last_name_element = 'test_last_name'
            employeesPage.email_element = 'test.test@test.com'
            employeesPage.phone_number_element = '226-123-4567'
            employeesPage.salary_element = '123456'
            employeesPage.date_hired_element = '2023-05-30'
            employeesPage.birthday_element = '1992-07-13'
            employeesPage.click_submit()

            self.driver.implicitly_wait(3)
            assert employeesPage.is_any_employees_found(), 'Employee was not created correctly'

        def test_employees_invalid(self):
            dashboardPage = page.DashboardPage(self.driver)
            employeesPage = page.EmployeePage(self.driver)

            assert self.test_login_account()
            self.driver.implicitly_wait(3)
            assert dashboardPage.is_title_matches(firstName='ALREADY_CREATED_FIRSTNAME', lastName='ALREADY_CREATED_LASTNAME'), 'Dashboard title does not match'

            dashboardPage.click_employes_link()

            employee_count_before = employeesPage.get_employee_count()
            #will try to submit an employee with missing information
            employeesPage.first_name_element = 'test_first_name'
            employeesPage.salary_element = '123456'
            employeesPage.date_hired_element = '2023-05-30'
            employeesPage.birthday_element = '1992-07-13'
            employeesPage.click_submit

            self.driver.implicitly_wait(3)
            employee_count_after = employeesPage.get_employee_count()

            assert employee_count_before == employee_count_after, 'Employee was created with missing information'


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()