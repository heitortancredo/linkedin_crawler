# -*- coding: utf-8 -*-
# Use Ex:
# scrapy crawl linkedin_spider -a login="yourmail@mail.com"
#                               -a password="yourpassword" -a perfil=ppizarro
import time
import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

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
        time.sleep(5)

        self.contact_info['infos'] = {}

        elem = self.get_element(self.driver, "class_name",
                                "contact-see-more-less")
        if elem is not None:
            elem.click()
            # linkedin perfil
            self.contact_info['infos']['perfil_in'] = self.get_element(self.driver, "xpath",
                                 '//section[contains(@class, "ci-vanity-url")]/div').text

            # sites
            self.contact_info['infos']['sites'] = []
            elem = self.get_elements(self.driver, "xpath",
                                     '//section[contains(@class, "ci-websites")]/ul/li/a')
            for e in elem:
                if e is not None:
                    self.contact_info['infos']['sites'].append(e.get_attribute("href"))

            # telefones
            self.contact_info['infos']['fones'] = []
            elem = self.get_elements(self.driver, "xpath",
                                     '//section[contains(@class, "ci-phone")]/ul/li/div')
            for e in elem:
                if e is not None:
                    self.contact_info['infos']['fones'].append(e.text)

            # emails
            self.contact_info['infos']['emails'] = []
            elem = self.get_elements(self.driver, "xpath",
                                     '//section[contains(@class, "ci-email")]/div')
            for e in elem:
                if e is not None:
                    self.contact_info['infos']['emails'].append(e.text)

            # twitter
            e = self.get_element(self.driver, "xpath", \
                                 '//section[contains(@class, "ci-twitter")]/ul/li/a')
            if e is not None:
                self.contact_info['infos']['twitter'] = e.get_attribute("href")

            # instant messenger
            elem = self.get_elements(self.driver, "xpath",
                                     '//section[contains(@class, "ci-ims")]/div')
            for e in elem:
                if e is not None:
                    self.contact_info['infos']['ims'] = e.text

            # aniversario
            e = self.get_element(self.driver, "xpath",
                                 '//section[contains(@class, "ci-birthday")]/div')
            if e is not None:
                self.contact_info['infos']['birthday'] = e.text

        self.contact_info['infos']['nome'] = self.get_element(self.driver, "xpath",
                                                              '//h1[contains(@class, "pv-top-card-section__name")]').text

        self.contact_info['infos']['cargo'] = self.get_element(self.driver, "xpath",
                                                               '//h2[contains(@class, "pv-top-card-section__headline")]').text

        self.contact_info['infos']['empresa'] = self.get_element(self.driver, "xpath",
                                                                 '//h3[contains(@class, "pv-top-card-section__company")]').text

        self.contact_info['infos']['local'] = self.get_element(self.driver, "xpath",
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
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #        self.driver.find_element_by_xpath('//body').send_keys(Keys.CONTROL+Keys.END)

        # SKILLZ
        self.contact_info['skills'] = []

        elem = self.get_element(self.driver, "xpath",
                                '//div[contains(@class, "profile-detail")]/div[5]/section/button')
        if elem is not None:
            elem.click()

            skills = self.get_elements(self.driver, "xpath",
                                       '//li[contains(@class, "pv-skill-entity--featured")]/div/div/a/div/span[1]')

            for skl in skills:
                self.contact_info['skills'].append(skl.text)

            # Linkedin muda o padrao do xpath das skills
            skills = self.get_elements(self.driver, "xpath",
                                       '//li[contains(@class, "pv-skill-entity--featured")]/div/div/div/span')
            for skl in skills:
                self.contact_info['skills'].append(skl.text)

        # CONQUISTAS
        self.contact_info['idiomas'] = []

        elem = self.get_element(self.driver, "xpath",
                                '//section[contains(@class, "languages")]\
                                /div/div[2]/button')
        if elem is not None:
            elem.click()
            time.sleep(1)

            idiomas =  self.get_elements(self.driver, "xpath",
                                         '//section[contains(@class, "languages")]/div/div/ul/li')

            for i in idiomas:
                self.contact_info['idiomas'].append(i.text)

        print "\nContact Info:\n"
        for i in self.contact_info['infos']:
            print self.contact_info['infos'][i]

        print "\nLanguages:\n"
        for l in self.contact_info['idiomas']:
            print l

        print "\nSkills: \n"
        for skl in self.contact_info['skills']:
            print skl

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
