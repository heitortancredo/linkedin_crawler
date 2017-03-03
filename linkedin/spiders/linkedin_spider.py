# -*- coding: utf-8 -*-
# Use Ex: scrapy crawl linkedin_spider -a login="yourmail@mail.com" -a heitortancredo password="yourpassword" -a perfil=ppizarro

import time
import json

from selenium import webdriver

from scrapy.spiders.init import InitSpider
from scrapy.http import Request


class LinkedinSpider(InitSpider):
    name = "linkedin_spider"
    allowed_domains = ["linkedin.com"]
#    start_urls = ['https://www.linkedin.com/']
#    perfil_urls = ['https://www.linkedin.com/in/ppizarro',
#                  'https://www.linkedin.com/in/viniciusbossle'
#                  ]
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
        login = self.driver.find_element_by_name('session_key')
        password = self.driver.find_element_by_name('session_password')
        login.send_keys(self.login)
        password.send_keys(self.password)
        btn = self.driver.find_element_by_name("signin")
        btn.click()

#        time.sleep(5)

        yield Request(self.perfil_url, cookies=self.driver.get_cookies(), callback=self.parse)


    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(3) # como eh assincrono preciso esperar o carregamento da pagina

#        print self.driver.page_source.encode('utf-8')

        info = self.driver.find_element_by_class_name("contact-see-more-less")
        info.click()
#        time.sleep(1)

        self.contact_info['nome'] = self.driver.find_element_by_xpath('//h1[contains(@class, "pv-top-card-section__name")]').text
        self.contact_info['cargo'] = self.driver.find_element_by_xpath('//h2[contains(@class, "pv-top-card-section__headline")]').text
        self.contact_info['empresa'] = self.driver.find_element_by_xpath('//h3[contains(@class, "pv-top-card-section__company")]').text
        self.contact_info['local'] = self.driver.find_element_by_xpath('//h3[contains(@class, "pv-top-card-section__location")]').text

        infos_label = self.driver.find_elements_by_class_name("pv-contact-info__header")
        infos_value = self.driver.find_elements_by_xpath('//*[contains(@class, "pv-contact-info__contact-item")] | //*[contains(@class, "pv-contact-info__action")]')
        # TODO: tratar sublistas (pode acontecer de um campo retornar uma lista de valores (Ex.: mais de um telefone))

        for k, v in zip(infos_label, infos_value):
            self.contact_info[k.text.lower()] = v.text

#        time.sleep(1)

#       Pegando informacoes da secao experiencia

        self.contact_position = self.driver.find_element_by_xpath('//*[contains(@class, "pv-profile-section__card-item position-entity")]/a')


#       Pegando informacoes da secao 'Conquistas'
#        info = self.driver.find_element_by_class_name("pv-recent-activity-section__see-more-inline")
#        info = self.driver.find_element_by_xpath('//*[contains(@class, "pv-profile-section__see-more-inline")]')
#        info.click()
#        time.sleep(2)
#        self.contact_accomp['idiomas'] = self.driver.find_elements_by_xpath('//section[contains(@class, "pv-profile-section")]/div/')
#        self.contact_accomp['idiomas'] = self.driver.find_elements_by_xpath('//section[contains(@class, "pv-profile-section")]/div/text()')

#       Pegando informacoes da secao 'Competencias'
#        skills = self.driver.find_element_by_xpath('//*[contains(@class, "artdeco-container-card-action-bar")]')
#        skills.click()
#        time.sleep(2)


#        self.contact_skills = self.driver.find_elements_by_xpath('//span[contains(@class, "pv-skill-entity__skill-name")]')
#        teste = self.driver.find_element_by_xpath('//span[contains(@class, "pv-skill-entity__skill-name"]')

        print "\n\n\n\n------------------"
        for info in self.contact_info:
            print info + " : " + self.contact_info[info]

        print "Perfil Linkedin empresa atual: " + self.contact_position.get_attribute("href")
#        print "Experiencia: \n"
#        for pos in self.contact_position:
#            print "-\n"
#            print pos.text

#       print "Idiomas:\n"
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
