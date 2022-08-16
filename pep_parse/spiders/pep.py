import scrapy
import re


NUM_NAM = r'PEP\s(?P<number>\d+)\W+(?P<name>.+)$'


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['http://peps.python.org/']

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get().replace('"', '')
        number, name = re.search(NUM_NAM, title).groups()
        status = response.xpath(
            '//*[contains(text(), "Status")]//'
            'following-sibling::node()[2]/text()'
        ).get()
        yield {
            'number': number,
            'name': name,
            'status': status,
        }

    def parse(self, response):
        pep_list = response.css('section[id="numerical-index"]')
        pep_links = pep_list.css('a[class="pep reference internal"]')
        for pep_link in pep_links:
            yield response.follow(pep_link, callback=self.parse_pep)
