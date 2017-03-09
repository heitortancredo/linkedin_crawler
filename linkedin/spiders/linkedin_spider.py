# -*- coding: utf-8 -*-
# Use Ex:
# scrapy crawl linkedin_spider -a login="yourmail@mail.com"
#                               -a password="yourpassword" -a perfil=ppizarro

import time
import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


from scrapy.spiders.init import InitSpider
from scrapy.http import Request


class LinkedinSpider(InitSpider):
    name = "linkedin_spider"
    allowed_domains = ["linkedin.com"]
#    start_urls = ['https://www.linkedin.com/']
#    perfil_url = 'https://www.linkedin.com/in/ppizarro'
#                  'https://www.linkedin.com/in/viniciusbossle'
#    perfil_url = 'https://www.linkedin.com/in/fabiano-michels-41479012a'

    contact_info = {}
    contact_accomp = {}

    def __init__(self, login, password, perfil):
        self.login = login
        self.password = password
        self.perfil_url = "https://www.linkedin.com/in/%s" % perfil

    def init_request(self):
        self.driver = webdriver.PhantomJS()
        self.driver.maximize_window()

#        self.driver = webdriver.Chrome("/usr/local/bin/chromedriver")
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

        elem = self.get_element(self.driver, "class_name",
                                "contact-see-more-less")
        if elem is not None:
            elem.click()
            time.sleep(1)

            infos_label = self.get_elements(self.driver, "class_name",
                                            "pv-contact-info__header")

            infos_value = self.get_elements(self.driver, "xpath",
                    '//*[contains(@class, "pv-contact-info__contact-item")] | \
                    //*[contains(@class, "pv-contact-info__action")]')

            # TODO: tratar sublistas (pode acontecer de um campo retornar uma
            # lista de valores (Ex.: mais de um telefone))

            for k, v in zip(infos_label, infos_value):
                if k and v:
                    self.contact_info[k.text.lower()] = v.text

        self.contact_info['nome'] = self.get_element(self.driver, "xpath",
            '//h1[contains(@class, "pv-top-card-section__name")]').text

        self.contact_info['cargo'] = self.get_element(self.driver, "xpath",
            '//h2[contains(@class, "pv-top-card-section__headline")]').text

        self.contact_info['empresa'] = self.get_element(self.driver, "xpath",
            '//h3[contains(@class, "pv-top-card-section__company")]').text

        self.contact_info['local'] = self.get_element(self.driver, "xpath",
            '//h3[contains(@class, "pv-top-card-section__location")]').text

        elem = self.get_element(self.driver, "class_name",
                                "truncate-multiline--button")
        if elem is not None:
            elem.click()
            time.sleep(1)

            self.contact_info['resumo'] = self.get_element(
                self.driver, "class_name",
                "pv-top-card-section__summary"
            ).text

#       Pegando informacoes da secao experiencia
        self.contact_info['in_empresa'] = self.get_element(self.driver, "xpath",
            '//*[contains(@class, \
            "pv-profile-section__card-item position-entity")]/a'
        ).get_attribute('href')


#       Pegando informacoes da secao 'Conquistas'
#        info = self.driver.find_element_by_class_name("pv-recent-activity-section__see-more-inline")
#        self.driver.execute_script("return arguments[0].scrollIntoView();", info)
#        info.click()
#        time.sleep(2)
#        self.contact_accomp['idiomas'] = self.driver.find_elements_by_xpath('//section[contains(@class, "pv-profile-section")]/div/')
#        self.contact_accomp['idiomas'] = self.driver.find_elements_by_xpath('//section[contains(@class, "pv-profile-section")]/section[3]')
#        self.contact_accomp['idiomas'] =  self.driver.find_element_by_xpath('//div[contains(@class, "pv-accomplishment-entity__title")]')

#        print self.driver.page_source.encode('utf-8')

#        print "\n\n\n\n------------------"
#        for info in self.contact_info:
#            print info + " : " + self.contact_info[info]

#        print "Experiencia: \n"
#        for pos in self.contact_position:
#            print "-\n"
#            print pos.text

#        print "Idiomas:\n"
#        print self.contact_accomp['idiomas']
#        for accomp in self.contact_accomp['idiomas']:
#            print "- " + accomp
#        print teste

#        print "Skills: \n"
#        for skill in self.contact_skills:
#            print skill
#        print teste
        print "------------------\n"
        print "JSON: " + json.dumps(self.contact_info)
        print "------------------\n\n\n"
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
