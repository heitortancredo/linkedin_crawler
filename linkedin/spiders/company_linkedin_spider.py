# -*- coding: utf-8 -*-
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from scrapy.spiders.init import InitSpider
from scrapy.http import Request


class CompanyLinkedinSpiderSpider(InitSpider):
    name = "company_linkedin_spider"
    allowed_domains = ["linkedin.com"]

    company_info = {}
    company_info["semelhantes"] = {}
    company_info["funcionarios"] = {}

    def __init__(self, login, password, perfil):
        self.login = login
        self.password = password
        self.perfil = perfil
        self.perfil_url = "https://www.linkedin.com/company-beta/%s" % self.perfil

    def init_request(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1920, 1080)

        # self.driver = webdriver.Chrome("/usr/local/bin/chromedriver")
        self.driver.get("http://www.linkedin.com/uas/login")

        btn = self.get_element(self.driver, "name", "signin")

        if btn is not None:
            login = self.get_element(self.driver, "name", "session_key")
            password = self.get_element(self.driver, "name", "session_password")
            if login and password is not None:
                login.send_keys(self.login)
                password.send_keys(self.password)
                btn.click()
                time.sleep(1)

        yield Request(self.perfil_url, cookies=self.driver.get_cookies(),
                      callback=self.parse)

    def parse(self, response):

        self.driver.get(response.url)
        # Como eh assincrono preciso esperar o carregamento da pagina
        self.scrolldown(self.driver)

        elem = self.get_element(self.driver, "xpath",
                                       '//img[contains(@class, "org-top-card-module__logo")]')
        if elem is not None:
            self.company_info["logo"] = elem.get_attribute("src")

        elem = self.get_element(self.driver, "class_name",
                                       "org-top-card-module__name")
        if elem is not None:
            self.company_info["nome"] = elem.text

        elem = self.get_element(self.driver, "class_name",
                                "org-about-company-module__specialities")
        if elem is not None:
            self.company_info["espcializacoes"] = elem.text

        elem = self.get_element(self.driver, "class_name",
                                "org-about-company-module__staff-count-range")
        if elem is not None:
            self.company_info["tamanho_empresa"] = elem.text

        elem = self.get_element(self.driver, "class_name",
                                "org-about-company-module__industry")
        if elem is not None:
            self.company_info["setor"] = elem.text

        elem = self.get_element(self.driver, "class_name",
                                "org-about-company-module__founded-year")
        if elem is not None:
            self.company_info["ano_fundacao"] = elem.text

        elem = self.get_element(self.driver, "class_name",
                                "org-about-company-module__headquarter")
        if elem is not None:
            self.company_info["sede"] = elem.text

        elem = self.get_element(self.driver, "xpath",
                                '//dd[contains(@class,\
                                "org-about-company-module__company-page-url")]/a')
        if elem is not None:
            self.company_info["url"] = elem.get_attribute("href")

        elem = self.get_element(self.driver, "class_name",
                                "org-about-us-organization-description__text")
        if elem is not None:
            self.company_info["sobre_nos"] = elem.text


        # SEMELHANTES

        elem = self.get_elements(self.driver, "class_name",
                                 "org-similar-companies-module__list-item")
        for e in elem:
            nome = self.get_element(e, "xpath",
                                   './/h3[contains(@class, "org-company-card__company-name")]').text
            self.company_info[ 'semelhantes'][nome] = []
            url = self.get_element(e, "xpath",
                                   './/a[contains(@class, "company-name-link")]').get_attribute("href")
            self.company_info['semelhantes'][nome].append(url)
            tam_empresa = self.get_element(e, "xpath",
                                   './/dd[contains(@class, "company-size")]').text
            self.company_info['semelhantes'][nome].append(tam_empresa)
            setor = self.get_element(e, "xpath",
                                   './/dd[contains(@class, "company-industry")]').text
            self.company_info['semelhantes'][nome].append(setor)

        # FUNCIONARIOS

        func_url = "https://www.linkedin.com/search/results/people/?facetCurrentCompany=%s" % self.perfil

        self.driver.get(func_url)
        time.sleep(3) # FIXME: WebDriver explicit wait?

       # print self.driver.page_source.encode('utf-8')

        elem = self.get_elements(self.driver, "xpath",
#        elem = self.driver.find_elements_by_xpath(
#            'li[contains(@class, "search-result__occluded-item")]')
            '//div[contains(@class, "search-results")]/div/div/ul/li')

        for e in elem:
            nome = self.get_element(e, "xpath",
                                   './/span[contains(@class, "actor-name")]').text
            self.company_info['funcionarios'][nome] = []

            in_profile = self.get_element(e, "xpath",
                                   './/div[contains(@class,\
                                          "search-result__info")]/a').get_attribute("href")
            self.company_info['funcionarios'][nome].append(in_profile)

            cargo = self.get_element(e, "xpath",
                                   './/div[contains(@class,\
                                     "search-result__info")]/p').text
            self.company_info['funcionarios'][nome].append(cargo)


        self.driver.close()
        yield self.company_info


    # FUNCOES AUXILIARES

    def get_element(self, web_driver, type_xpath, xpath_string):

        try:
            if type_xpath == "class_name":
                return web_driver.find_element_by_class_name(xpath_string)
            if type_xpath == "xpath":
                return web_driver.find_element_by_xpath(xpath_string)
            if type_xpath == "name":
                return web_driver.find_element_by_name(xpath_string)

        except NoSuchElementException:
            self.logger.error(xpath_string)
            return None

    def get_elements(self, web_driver, type_xpath, xpath_string):
        try:
            if type_xpath == "class_name":
                return web_driver.find_elements_by_class_name(xpath_string)
            if type_xpath == "xpath":
                return web_driver.find_elements_by_xpath(xpath_string)
            if type_xpath == "name":
                return web_driver.find_elements_by_name(xpath_string)

        except NoSuchElementException:
            self.logger.error(xpath_string)
            return None

    def scrolldown(self, web_driver):
        web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

