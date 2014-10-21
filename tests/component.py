import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

class BaseComponent(object):
    def __init__(self, driver):
        self.driver = driver

    def find(self, locator):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element(locator[0], locator[1])
        )

    def find_send(self, locator, key):
        element = self.find(locator)
        for i in xrange(5):
            try:
                element.send_keys(key)
                break
            except Exception:
                pass



    def find_click(self, locator):
        element = self.find(locator)
        for i in xrange(5):
            try:
                element.click()
                break
            except Exception:
                pass


class AuthForm(BaseComponent):
    LOGIN = (By.ID, 'id_Login')
    PASSWORD = (By.ID, 'id_Password')
    SUBMIT = (By.CSS_SELECTOR, '#gogogo>input')

    def set_login(self, login):
        self.find_send(self.LOGIN, login)

    def set_password(self, pwd):
        self.find_send(self.PASSWORD, pwd)

    def submit(self):
        self.find_click(self.SUBMIT)


class IncomeSelector(BaseComponent):
    LOW = (By.ID, "income_group-9286")
    MEDIUM = (By.ID, "income_group-9287")
    HIGH = (By.ID, "income_group-9288")
    GROUP = (By.CSS_SELECTOR, ".campaign-setting__wrapper_income_group .campaign-setting__value")

    def __init__(self, driver):
        self.driver = driver
        self.find_click(self.GROUP)

    def select_high(self):
        self.find_click(self.HIGH)

    def select_medium(self):
        self.find_click(self.MEDIUM)

    def select_low(self):
        self.find_click(self.LOW)

    def get_high(self):
        return self.find(self.HIGH).is_selected()

    def get_medium(self):
        return self.find(self.MEDIUM).is_selected()

    def get_low(self):
        return self.find(self.LOW).is_selected()


class CompanyTimeSelector(BaseComponent):
    FROM = (By.XPATH, '//input[@class="campaign-setting__detail__date-input hasDatepicker"][@data-name="from"]')
    TO = (By.XPATH, '//input[@class="campaign-setting__detail__date-input hasDatepicker"][@data-name="to"]')
    GROUP = (By.CSS_SELECTOR, ".campaign-setting__wrapper_date .campaign-setting__value")

    def __init__(self, driver):
        self.driver = driver
        self.find_click(self.GROUP)

    def set_from(self, from_date):
        self.find_send(self.FROM, from_date)

    def set_to(self, to_date):
        self.find_send(self.TO, to_date)

    def get_from(self):
        return self.find(self.FROM).get_attribute("value")

    def get_to(self):
        return self.find(self.TO).get_attribute("value")

    def update(self):
        self.find_send(self.TO, Keys.RETURN)


class PlatformSelector(BaseComponent):
    TYPE = (By.ID, 'product-type-6039')
    MOBILE = (By.ID, 'pad-mobile_app_mobile_service')

    def select_mobile_platform(self):
        self.find_click(self.TYPE)
        self.find_click(self.MOBILE)


class BannerCreator(BaseComponent):
    PICTURE = (By.XPATH, '//input[@data-name="image"][@type="file"]')
    LINK = (By.XPATH, '//li[@data-top="false"]/span/input[@class="banner-form__input"][@data-name="url"]')
    BUTTON = (By.CSS_SELECTOR, '.banner-form__save-button')
    BANNER = (By.CSS_SELECTOR, '.added-banner')
    BANNER_PREVIEW = (By.CSS_SELECTOR, '.banner-preview__img')

    def set_picture(self, path):
        path = os.path.abspath(path)
        self.find_send(self.PICTURE, path)

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element(self.BANNER_PREVIEW[0], self.BANNER_PREVIEW[1])
            .value_of_css_property("display") == 'block'
        )

    def set_link(self, link):
        self.find_send(self.LINK, link)

    def submit(self):
        self.find_click(self.BUTTON)
        self.find(self.BANNER)


class TopMenu(BaseComponent):
    EMAIL = (By.CSS_SELECTOR, '#PH_user-email')

    def get_email(self):
        return self.find(self.EMAIL).text