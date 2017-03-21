import os

from scrapy.crawler import CrawlerProcess
from scrapy import signals


class PersonCrawler():
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'project.settings')


    def run_crawler(self, perfil):
        results = []
        settings = {
            'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3)\
            AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8',
            'DOWNLOAD_DELAY': '3',
            'BOT_NAME': 'linkedin',

            'SPIDER_MODULES': ['linkedin.spiders'],
            'NEWSPIDER_MODULE': 'linkedin.spiders',
        }

        def _add_item(item):
            results.append(item)

        process = CrawlerProcess(settings)
        crawler = process.create_crawler("linkedin_spider")
        crawler.signals.connect(_add_item, signals.item_passed)
        process.crawl(crawler, self.login, self.senha, perfil)
        process.start()

        return results
