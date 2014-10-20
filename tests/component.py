import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

class BaseComponent(object):
    def __init__(self, driver):
        self.driver = driver


class AuthForm(BaseComponent):
    LOGIN = 'id_Login'
    PASSWORD = 'id_Password'
    SUBMIT = '#gogogo>input'

    def set_login(self, login):
        self.driver.find_element_by_id(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_id(self.PASSWORD).send_keys(pwd)

    def submit(self):
        self.driver.find_element_by_css_selector(self.SUBMIT).click()


class IncomeSelector(BaseComponent):
    LOW_ID = "income_group-9286"
    MEDIUM_ID = "income_group-9287"
    HIGH_ID = "income_group-9288"
    GROUP_CSS = ".campaign-setting__wrapper_income_group .campaign-setting__value"

    def __init__(self, driver):
        self.driver = driver
        self.driver.find_element_by_css_selector(self.GROUP_CSS).click()

    def select_high(self):
        self.driver.find_element_by_id(self.HIGH_ID).click()

    def select_medium(self):
        self.driver.find_element_by_id(self.MEDIUM_ID).click()

    def select_low(self):
        self.driver.find_element_by_id(self.LOW_ID).click()

    def get_high(self):
        return self.driver.find_element_by_id(self.HIGH_ID).is_selected()

    def get_medium(self):
        return self.driver.find_element_by_id(self.MEDIUM_ID).is_selected()

    def get_low(self):
        return self.driver.find_element_by_id(self.LOW_ID).is_selected()


class CompanyTimeSelector(BaseComponent):
    FROM_XPATH = '//input[@class="campaign-setting__detail__date-input hasDatepicker"][@data-name="from"]'
    TO_XPATH = '//input[@class="campaign-setting__detail__date-input hasDatepicker"][@data-name="to"]'
    GROUP_CSS = ".campaign-setting__wrapper_date .campaign-setting__value"

    def __init__(self, driver):
        self.driver = driver
        WebDriverWait(self.driver, 30, 0.1).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, self.GROUP_CSS))
        ).click()

    def set_from(self, from_date):
        self.driver.find_element_by_xpath(self.FROM_XPATH).send_keys(from_date)

    def set_to(self, to_date):
        self.driver.find_element_by_xpath(self.TO_XPATH).send_keys(to_date)

    def get_from(self):
        return self.driver.find_element_by_xpath(self.FROM_XPATH).get_attribute("value")

    def get_to(self):
        return self.driver.find_element_by_xpath(self.TO_XPATH).get_attribute("value")

    def update(self):
        self.driver.find_element_by_xpath(self.TO_XPATH).send_keys(Keys.RETURN)


class PlatformSelector(BaseComponent):
    def select_mobile_platform(self):
        self.driver.find_element_by_id('product-type-6039').click()

        WebDriverWait(self.driver, 30, 1).until(
            expected_conditions.presence_of_element_located((By.ID, 'pad-mobile_app_mobile_service'))
        ).click()


class BannerCreator(BaseComponent):
    PICTURE_XPATH = '//input[@data-name="image"][@type="file"]'
    LINK_XPATH = '//li[@data-top="false"]/span/input[@class="banner-form__input"][@data-name="url"]'
    BUTTON_CSS = '.banner-form__save-button'
    BANNER_CSS = '.added-banner'

    def set_picture(self, path):
        path = os.path.abspath(path)
        self.driver.find_element_by_xpath(self.PICTURE_XPATH).send_keys(path)
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector('.banner-preview .banner-preview__img')
            .value_of_css_property("display") == 'block'
        )

    def set_link(self, link):
        self.driver.find_element_by_xpath(self.LINK_XPATH).send_keys(link)

    def submit(self):
        self.driver.find_element_by_css_selector(self.BUTTON_CSS).click()
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, self.BANNER_CSS))
        )


class TopMenu(BaseComponent):
    EMAIL = '#PH_user-email'

    def get_email(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.EMAIL).text
        )