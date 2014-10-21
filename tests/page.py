import urlparse

from selenium.webdriver.common.by import By
from component import BaseComponent, AuthForm, IncomeSelector, CompanyTimeSelector, PlatformSelector, BannerCreator, TopMenu


class Page(BaseComponent):
    BASE_URL = 'https://target.mail.ru'
    PATH = ''

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
    CREATE = (By.CSS_SELECTOR, '.main-button__label')
    BANNER = (By.CSS_SELECTOR, '.added-banner')

    def __init__(self, driver):
        self.driver = driver
        self.iselector = None
        self.cselector = None

    @property
    def create_button(self):
        return self.find(self.CREATE)

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
        return self.find(self.BANNER)


class CampaignsPage(Page):
    PATH = '/ads/campaigns/'
    EDIT = (By.CSS_SELECTOR, '.control__link_edit')

    @property
    def edit_button(self):
        return self.find(self.EDIT)