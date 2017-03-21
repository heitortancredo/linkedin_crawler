# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


from scrapy.spiders.init import InitSpider
from scrapy.http import Request


class CompanyLinkedinSpider(InitSpider):
    name = "company_linkedin_spider"
    allowed_domains = ["linkedin.com"]

    company_info = {}
    company_info["relates"] = {}
    company_info["company_employees"] = {}

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

        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.NAME, "signin"))
            )
        except TimeoutException:
            self.logger.critical("Nao foi possivel efetuar o login")
            self.driver.quit()
            yield self.company_info


        btn = self.get_element(self.driver, "name", "signin")

        if btn is not None:
            login = self.get_element(self.driver, "name", "session_key")
            password = self.get_element(self.driver, "name", "session_password")
            if login and password is not None:
                login.send_keys(self.login)
                password.send_keys(self.password)
                btn.click()

        yield Request(self.perfil_url, cookies=self.driver.get_cookies(),
                      callback=self.parse)

    def parse(self, response):

        self.driver.get(response.url)
        # Como eh assincrono preciso esperar o carregamento da pagina
        try:
            elem = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "org-similar-companies-module__list-item"))
            )
        except TimeoutException:
            self.logger.critical("Nao foi possivel carregar a pagina")
            self.driver.quit()
            yield self.company_info

        self.scrolldown(self.driver)

        elem = self.get_element(self.driver, "id",
                                "org-about-company-module__show-details-btn")
        if elem is not None:
            elem.click()

        elem = self.get_element(self.driver, "xpath",
                                       '//img[contains(@class, "org-top-card-module__logo")]')
        if elem is not None:
            self.company_info["logo"] = elem.get_attribute("src")

        elem = self.get_element(self.driver, "class_name",
                                       "org-top-card-module__name")
        if elem is not None:
            self.company_info["name"] = elem.text

        elem = self.get_element(self.driver, "class_name",
                                "org-about-company-module__specialities")
        if elem is not None:
            self.company_info["specialities"] = elem.text

        elem = self.get_element(self.driver, "class_name",
                                "org-about-company-module__staff-count-range")
        if elem is not None:
            self.company_info["employees"] = elem.text

        elem = self.get_element(self.driver, "class_name",
                                "org-about-company-module__industry")
        if elem is not None:
            self.company_info["category_industry"] = elem.text

        elem = self.get_element(self.driver, "class_name",
                                "org-about-company-module__founded-year")
        if elem is not None:
            self.company_info["start"] = elem.text

        elem = self.get_element(self.driver, "class_name",
                                "org-about-company-module__headquarter")
        if elem is not None:
            self.company_info["address_city"] = elem.text

        elem = self.get_element(self.driver, "xpath",
                                '//dd[contains(@class,\
                                "org-about-company-module__company-page-url")]/a')
        if elem is not None:
            self.company_info["url"] = elem.get_attribute("href")

        elem = self.get_element(self.driver, "class_name",
                                "org-about-us-organization-description__text")
        if elem is not None:
            self.company_info["description"] = elem.text


        # SEMELHANTES

        elem = self.get_elements(self.driver, "class_name",
                                 "org-similar-companies-module__list-item")
        for e in elem:
            nome = self.get_element(e, "xpath",
                                   './/h3[contains(@class, "org-company-card__company-name")]').text
            self.company_info[ 'relates'][nome] = []
            url = self.get_element(e, "xpath",
                                   './/a[contains(@class, "company-name-link")]').get_attribute("href")
            self.company_info['relates'][nome].append(url)
            tam_empresa = self.get_element(e, "xpath",
                                   './/dd[contains(@class, "company-size")]').text
            self.company_info['relates'][nome].append(tam_empresa)
            setor = self.get_element(e, "xpath",
                                   './/dd[contains(@class, "company-industry")]').text
            self.company_info['relates'][nome].append(setor)

        # FUNCIONARIOS

        func_url = "https://www.linkedin.com/search/results/people/?facetCurrentCompany=%s" % self.perfil

        self.driver.get(func_url)
#        elem = self.get_element(self.driver, "xpath", '//span[contains(@class,\
#                                "org-company-employees-snackbar__see-all-employees-link")]/a')
#        elem.click()

        try:
            elem = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//div[contains(@class,\
                                                "search-results")]/div/div/ul/li'))
            )
        except TimeoutException:
            self.logger.critical("Nao foi possivel carregar a pagina de funcionarios")
            self.driver.quit()
            yield self.company_info

        elem = self.get_elements(self.driver, "xpath",
            '//div[contains(@class, "search-results")]/div/div/ul/li')

        for e in elem:
            nome = self.get_element(e, "xpath",
                                   './/span[contains(@class, "actor-name")]').text
            self.company_info['company_employees'][nome] = []

            in_profile = self.get_element(e, "xpath",
                                   './/div[contains(@class,\
                                          "search-result__info")]/a').get_attribute("href")
            self.company_info['company_employees'][nome].append(in_profile)

            cargo = self.get_element(e, "xpath",
                                   './/div[contains(@class,\
                                     "search-result__info")]/p').text
            self.company_info['company_employees'][nome].append(cargo)

            # TODO: navegar na paginacao dos resultados para pegar os demais
            # funcionarios, como estah eh feito o crawler apenas da primeira
            # pagina de resultados


        self.driver.quit()
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
            if type_xpath == "id":
                return web_driver.find_element_by_id(xpath_string)

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
            if type_xpath == "id":
                return web_driver.find_elements_by_id(xpath_string)

        except NoSuchElementException:
            self.logger.error(xpath_string)
            return None

    def scrolldown(self, web_driver):
        web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

