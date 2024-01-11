from locators import HomePageLocators, RegisterPageLocators, LoginPageLocators, DashboardPageLocators, PositionPageLocators, DepartmentsPageLocators, EmployeePageLocators
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
        print('EXPECTED: Login' )
        print('ACTUAL:', self.driver.title)
        return 'Login' == self.driver.title

    def is_login_failed(self)-> bool:
        return 'Username not found.' in self.driver.page_source 

    def click_submit(self):
        element = self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON)
        element.click()

class DashboardPage(BasePage):

    def is_title_matches(self, firstName, lastName)-> bool:
        print('EXPECTED: ', f"{firstName} {lastName}'s Dashboard" )
        print('ACTUAL:', self.driver.title)
        return f"{firstName} {lastName}'s Dashboard" == self.driver.title
    
    def click_positions_link(self):
        element = self.driver.find_element(*DashboardPageLocators.POSITION_BUTTON)
        element.click()

    def click_departments_link(self):
        element = self.driver.find_element(*DashboardPageLocators.DEPARTMENT_BUTTON)
        element.click()

    def click_employes_link(self):
        element = self.driver.find_element(*DashboardPageLocators.EMPLOYEE_BUTTON)
        element.click()
    
class PositionPage(BasePage):

    title_element = PositionTitleElements()
    description_element = PositionDescriptionElements()
    base_pay_elements = PositionBasePayElements()

    def is_title_matches(self)-> bool:
        return 'Positions' == self.driver.title
    
    def click_submit(self):
        element = self.driver.find_element(*PositionPageLocators.SUBMIT_BUTTON)
        element.click()

    def is_any_position_found(self):
        return 'No matching records found.' not in self.driver.page_source

    def is_position_not_found(self, position_title):
        return position_title not in self.driver.page_source
    
    def get_position_count(self):
        return int(self.driver.find_element(*PositionPageLocators.POSITION_COUNT).text)

class DepartmentPage(BasePage):
    def is_title_matches(self)-> bool:
        return 'Departments' == self.driver.title
    
    title_element = DepartmentTitleElements()
    description_element = DepartmentDescriptionElements()

    def click_submit(self):
        element = self.driver.find_element(*DepartmentsPageLocators.SUBMIT_BUTTON)
        element.click()

    def is_any_departments_found(self):
        return 'No matching records found.' not in self.driver.page_source
    
    def get_department_count(self):
        return int(self.driver.find_element(*DepartmentsPageLocators.DEPARTMENT_COUNT).text)
    
class EmployeePage(BasePage):
    def is_title_matches(self)-> bool:
        return 'Employees' == self.driver.title
    
    first_name_element = EmployeeFirstNameElements()
    last_name_element = EmployeeLastNameElements()
    email_element = EmployeeEmailElements()
    phone_number_element = EmployeePhoneNumberElements()
    salary_element = EmployeeSalaryElements()
    date_hired_element = EmployeeDateHiredElements()
    birthday_element = EmployeeBirthdayElements()

    def is_any_employees_found(self):
        return 'No matching records found.' not in self.driver.page_source
    
    def get_employee_count(self):
        return int(self.driver.find_element(*EmployeePageLocators.EMPLOYEE_COUNT).text)
    
    def click_submit(self):
        element = self.driver.find_element(*EmployeePageLocators.SUBMIT_BUTTON)
        element.click()