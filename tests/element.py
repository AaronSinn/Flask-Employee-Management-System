from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

class BasePageElements():
    def __set__(self, obj, value):
        print('obj:', obj)
        driver = obj.driver
    
        WebDriverWait(driver, timeout=100).until(
            lambda driver: driver.find_element(By.ID, self.locator))
        
        driver.find_element(By.ID, self.locator).clear()
        driver.find_element(By.ID, self.locator).send_keys(value)

    def __get__(self, obj, owner):
        print('owner:', owner)

        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(By.ID, self.locator))
        element = driver.find_element(By.ID, self.locator)
        return element.get_attribute("value")

class RegisterFirstNameElements(BasePageElements):
    locator = 'firstNameInput'

class RegisterLastNameElements(BasePageElements):
    locator = 'lastNameInput'

class RegisterUsernameElements(BasePageElements):
    locator = 'usernameInput'

class RegisterPasswordElements(BasePageElements):
    locator = 'passwordInput'

class LoginUsernameElements(BasePageElements):
    locator = 'usernameInput'

class LoginPasswordElements(BasePageElements):
    locator = 'passwordInput'