import unittest
import os
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Remote

from page import AuthPage, CreatePage, CampaignsPage


class Tests(unittest.TestCase):
    LOGIN = 'tech-testing-ha2-3@bk.ru'

    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'FIREFOX')
        self.PASSWORD = os.environ['TTHA2PASSWORD']

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )
        
        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_form = auth_page.form
        auth_form.set_login(self.LOGIN)
        auth_form.set_password(self.PASSWORD)
        auth_form.submit()

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        create_page = CreatePage(self.driver)
        create_page.open()
        create_page.wait_for_load()

        assert create_page.top_menu.get_email() == self.LOGIN

    def test_date_bad_order(self):
        create_page = CreatePage(self.driver)
        create_page.open()
        create_page.wait_for_load()

        create_page.company_time_selector.set_from('30.12.2014')
        create_page.company_time_selector.set_to('10.12.2014')
        create_page.company_time_selector.update()

        assert create_page.company_time_selector.get_from() == '10.12.2014'
        assert create_page.company_time_selector.get_to() == '30.12.2014'

    def test_bad_date(self):
        create_page = CreatePage(self.driver)
        create_page.open()
        create_page.wait_for_load()

        create_page.company_time_selector.set_to('10.12.20000')
        create_page.company_time_selector.update()

        assert create_page.company_time_selector.get_to() != '10.12.20000'

    def test_add_banner(self):
        create_page = CreatePage(self.driver)
        create_page.open()
        create_page.wait_for_load()

        create_page.platform_selector.select_mobile_platform()

        banner_creator = create_page.banner_creator
        banner_creator.set_link('https://play.google.com/')
        banner_creator.set_picture('./pic.gif')
        banner_creator.submit()

        assert create_page.banner.is_displayed()

    def test_save_date(self):
        create_page = CreatePage(self.driver)
        create_page.open()
        create_page.wait_for_load()

        create_page.platform_selector.select_mobile_platform()

        banner_creator = create_page.banner_creator
        banner_creator.set_link('https://play.google.com/')
        banner_creator.set_picture('./pic.gif')
        banner_creator.submit()

        from_date = '02.12.2014'
        to_date = '30.06.2015'

        create_page.company_time_selector.set_from(from_date)
        create_page.company_time_selector.set_to(to_date)
        create_page.create_button.click()

        campagins_page = CampaignsPage(self.driver)
        campagins_page.edit_button.click()

        edit_page = CreatePage(self.driver)
        edit_page.wait_for_load()

        assert edit_page.company_time_selector.get_from() == from_date
        assert edit_page.company_time_selector.get_to() == to_date

    def test_save_income(self):
        create_page = CreatePage(self.driver)
        create_page.open()
        create_page.wait_for_load()

        create_page.platform_selector.select_mobile_platform()

        banner_creator = create_page.banner_creator
        banner_creator.set_link('https://play.google.com/')
        banner_creator.set_picture('./pic.gif')
        banner_creator.submit()

        create_page.income_selector.select_high()
        create_page.income_selector.select_low()

        create_page.create_button.click()

        campagins_page = CampaignsPage(self.driver)
        campagins_page.edit_button.click()

        edit_page = CreatePage(self.driver)
        edit_page.wait_for_load()

        assert edit_page.income_selector.get_high()
        assert not edit_page.income_selector.get_medium()
        assert edit_page.income_selector.get_low()