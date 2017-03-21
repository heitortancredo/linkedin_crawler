# -*- coding: utf-8 -*-
# Use Ex:
# scrapy crawl linkedin_spider -a login="yourmail@mail.com"
#                               -a password="yourpassword" -a perfil=ppizarro
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from scrapy.spiders.init import InitSpider
from scrapy.http import Request


class LinkedinSpider(InitSpider):
    name = "linkedin_spider"
    allowed_domains = ["linkedin.com"]

    contact_info = {}

    def __init__(self, login, password, perfil):
        self.login = login
        self.password = password
        self.perfil_url = "https://www.linkedin.com/%s" % perfil

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
            self.driver.close()
            yield self.contact_info

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
                EC.presence_of_element_located((By.XPATH,
                                                '//h2[contains(@class,\
                                                "pv-profile-section__card-heading")]'))
            )
        except TimeoutException:
            self.logger.critical("Nao foi possivel carregar a pagina")
            self.driver.close()
            yield self.contact_info

        self.contact_info['infos'] = {}
        self.contact_info['following'] = {}
        self.contact_info['skill_name'] = []
        self.contact_info['language_name'] = []

        elem = self.get_element(self.driver, "class_name",
                                "contact-see-more-less")
        if elem is not None:
            elem.click()

            # Foto perfil

            elem = self.get_element(self.driver, "class_name",
                                    "pv-top-card-section__image")
            if elem is not None:
                self.contact_info['infos']['foto'] = elem.get_attribute("src")

            # linkedin perfil
            self.contact_info['infos']['perfil_in'] = self.get_element(self.driver, "xpath",
                                 '//section[contains(@class, "ci-vanity-url")]/div').text

            # sites
            self.contact_info['infos']['site'] = []
            elem = self.get_elements(self.driver, "xpath",
                                     '//section[contains(@class, "ci-websites")]/ul/li/a')
            for e in elem:
                if e is not None:
                    self.contact_info['infos']['site'].append(e.get_attribute("href"))

            # telefones
            self.contact_info['infos']['phone'] = []
            elem = self.get_elements(self.driver, "xpath",
                                     '//section[contains(@class, "ci-phone")]/ul/li/div')
            for e in elem:
                if e is not None:
                    self.contact_info['infos']['phone'].append(e.text)

            # emails
            self.contact_info['infos']['email'] = []
            elem = self.get_elements(self.driver, "xpath",
                                     '//section[contains(@class, "ci-email")]/div')
            for e in elem:
                if e is not None:
                    self.contact_info['infos']['email'].append(e.text)

            # twitter
            e = self.get_element(self.driver, "xpath", \
                                 '//section[contains(@class, "ci-twitter")]/ul/li/a')
            if e is not None:
                self.contact_info['infos']['social_twitter_handle'] = e.get_attribute("href")

            # instant messenger
            elem = self.get_elements(self.driver, "xpath",
                                     '//section[contains(@class, "ci-ims")]/div')
            for e in elem:
                if e is not None:
                    self.contact_info['infos']['social_ims_handle'] = e.text

            # aniversario
            e = self.get_element(self.driver, "xpath",
                                 '//section[contains(@class, "ci-birthday")]/div')
            if e is not None:
                self.contact_info['infos']['dateofbirth'] = e.text

        self.contact_info['infos']['full_name'] = self.get_element(self.driver, "xpath",
                                                              '//h1[contains(@class, "pv-top-card-section__name")]').text

        self.contact_info['infos']['position_title'] = self.get_element(self.driver, "xpath",
                                                               '//h2[contains(@class, "pv-top-card-section__headline")]').text

        self.contact_info['infos']['position_company_name'] = self.get_element(self.driver, "xpath",
                                                                 '//h3[contains(@class, "pv-top-card-section__company")]').text
        """
        # tentando buscar o historico das empresas que ja trabalhou
        self.contact_info['infos']['empresas'] = {}
        elem = self.get_elements(self.driver, "xpath",
                                 '//li[contains(@class, "position-entity")]')

        for e in elem:
            if e is not None:
                self.contact_info['infos']['empresas'] = [e.text]

        """
        self.contact_info['infos']['address_summary'] = self.get_element(self.driver, "xpath",
                                                               '//h3[contains(@class, "pv-top-card-section__location")]').text


# ------[ INICIO do bloco para pegar o resumo]
#        elem = self.get_element(self.driver, "class_name",
#                                "truncate-multiline--button")
#        if elem is not None:
#            elem.click()
#
#            self.contact_info['infos']['resumo'] = self.get_element(
#                self.driver, "class_name",
#                "pv-top-card-section__summary"
#            ).text
# ------[ FIM do bloco para pegar o resumo]

#       Pegando informacoes da secao experiencia
        e = self.get_element(self.driver, "xpath", '//*[contains(@class, \
                             "pv-profile-section__card-item position-entity")]/a')
        if e is not None:
            self.contact_info['infos']['in_empresa'] = e.get_attribute("href")

        # Scroll Down
        self.scrolldown(self.driver)
        # self.driver.find_element_by_xpath('//body').send_keys(Keys.CONTROL+Keys.END)

        # SKILLZ

        elem = self.get_element(self.driver, "xpath",
                                '//div[contains(@class, "profile-detail")]/div[5]/section/button')
        if elem is not None:
            elem.click()

            skills = self.get_elements(self.driver, "xpath",
                                       '//li[contains(@class, "pv-skill-entity--featured")]/div/div/a/div/span[1]')

            for skl in skills:
                self.contact_info['skill_name'].append(skl.text)

            # Linkedin muda o padrao do xpath das skills
            skills = self.get_elements(self.driver, "xpath",
                                       '//li[contains(@class, "pv-skill-entity--featured")]/div/div/div/span')
            for skl in skills:
                self.contact_info['skill_name'].append(skl.text)

        # CONQUISTAS

        elem = self.get_element(self.driver, "xpath",
                                '//section[contains(@class, "languages")]\
                                /div/div[2]/button')
        if elem is not None:
            elem.click()
            try:
                elem = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located
                    ((By.XPATH, '//section[contains(@class, "languages")]/div/div/ul/li[2]'))
                )
            except TimeoutException:
                pass
            idiomas =  self.get_elements(self.driver, "xpath",
                                         '//section[contains(@class, "languages")]/div/div/ul/li')

            for i in idiomas:
                # Formato: Idioma "nome_idioma" Nivel "nivel de fluencia"
                self.contact_info['language_name'].append(i.text)

        # SEGUINDO
        self.contact_info['following']['peoples'] = []

        elem = self.get_element(self.driver, "xpath",
                                '//a[contains(@href, "/connections/")]/h2')
        if elem is not None:
            elem.click()
            try:
                elem = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located
                    ((By.CLASS_NAME, 'profile-item__name--has-hover'))
                )
            except TimeoutException:
                pass

            # Pessoas
            elem = self.get_elements(self.driver, "xpath", '//span[contains(@class,\
                                     "profile-item__name--has-hover")]')

            for e in elem:
                if e is not None:
                    self.contact_info['following']['peoples'].append(e.text)
            # TODO: * fazer scrolldown na subjanela para pegar mais pessoas
            #       * pegar o link do perfil

        # Empresas
        self.contact_info['following']['companies'] = []

        # scrolldown
        self.scrolldown(self.driver)

        elem = self.get_element(self.driver, "xpath", '//a[contains(@href,\
                                                 "/interests/")]/span')
        if elem is not None:
            elem.click()
            # elem = self.driver.find_element_by_xpath(
            #    '//a[contains(@href, "/interests/companies/")]')
            #elem.click()
            try:
                elem = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located
                    ((By.XPATH,
                      '//span[contains(@class, "pv-entity__summary-title--has-hover")]'))
                )
            except TimeoutException:
                pass
            elem = self.get_elements(self.driver, "xpath", '//span[contains(@class,\
                                    "pv-entity__summary-title--has-hover")]')

            for e in elem:
                if e is not None:
                    self.contact_info['following']['companies'].append(e.text)
            # TODO: * conseguir pegar apenas as empresas (clicar na secao empresas
            #         da subjanela)
            #       * pegar o link do perfil
        '''
        print "\nContact Info:\n"
        for i in self.contact_info['infos']:
            print self.contact_info['infos'][i]

        print "\nLanguages:\n"
        for l in self.contact_info['idiomas']:
            print l

        print "\nSkills: \n"
        for skl in self.contact_info['skills']:
            print skl
        '''
#        print "------------------\n"
#        print "JSON: " + json.dumps(self.contact_info)
#        print "------------------\n\n\n"
        self.driver.close()
        yield self.contact_info


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
