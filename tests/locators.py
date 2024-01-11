from selenium.webdriver.common.by import By

class HomePageLocators():
    REGISTER_LINK = (By.ID, 'regLink')
    LOGIN_LINK = (By.ID, 'loginLink')

class RegisterPageLocators():
    SUBMIT_BUTTON = (By.ID, 'submit')

class LoginPageLocators():
    LOGIN_BUTTON = (By.ID, 'submit')

class DashboardPageLocators():
    POSITION_BUTTON = (By.ID, 'positionsPageLink')
    DEPARTMENT_BUTTON = (By.ID, 'departmentsPageLink')
    EMPLOYEE_BUTTON = (By.ID, 'employeePageLink')

class PositionPageLocators():
    SUBMIT_BUTTON = (By.ID, 'submit')
    POSITION_COUNT = (By.XPATH, '/html/body/div[2]/div[1]/div/div/div[3]/div/div[1]/b[3]')

class DepartmentsPageLocators():
    SUBMIT_BUTTON = (By.ID, 'submit')
    DEPARTMENT_COUNT = (By.XPATH, '/html/body/div[2]/div[1]/div/div/div[3]/div/div[1]/b[3]')

class EmployeePageLocators():
    SUBMIT_BUTTON = (By.ID, 'submit')
    EMPLOYEE_COUNT = (By.XPATH, '/html/body/div[2]/div[1]/div/div/div[3]/div/div[1]/b[3]')
