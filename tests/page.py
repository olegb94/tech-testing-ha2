import urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from component import AuthForm, IncomeSelector, CompanyTimeSelector, PlatformSelector, BannerCreator, TopMenu


class Page(object):
    BASE_URL = 'https://target.mail.ru'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)


class AuthPage(Page):
    PATH = '/login'

    @property
    def form(self):
        return AuthForm(self.driver)


class CreatePage(Page):
    PATH = '/ads/create'
    CREATE_CSS = '.main-button__label'
    BANNER_CSS = '.added-banner'

    def __init__(self, driver):
        self.driver = driver
        self.iselector = None
        self.cselector = None

    def wait_for_load(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.CREATE_CSS)
        )

    @property
    def create_button(self):
        return self.driver.find_element_by_css_selector(self.CREATE_CSS)

    @property
    def income_selector(self):
        if self.iselector is None:
            self.iselector = IncomeSelector(self.driver)
        return self.iselector

    @property
    def company_time_selector(self):
        if self.cselector is None:
            self.cselector = CompanyTimeSelector(self.driver)
        return self.cselector

    @property
    def platform_selector(self):
        return PlatformSelector(self.driver)

    @property
    def banner_creator(self):
        return BannerCreator(self.driver)

    @property
    def top_menu(self):
        return TopMenu(self.driver)

    @property
    def banner(self):
        return WebDriverWait(self.driver, 30).until(
            lambda d: d.find_element_by_css_selector(self.BANNER_CSS)
        )


class CampaignsPage(Page):
    PATH = '/ads/campaigns/'
    EDIT_CSS = '.control__link_edit'

    @property
    def edit_button(self):
        return WebDriverWait(self.driver, 30).until(
            lambda d: d.find_element_by_css_selector(self.EDIT_CSS)
        )