from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from gnats.spiders.utils import parse_gnats_item, get_password
from mongodb import issues


user, password = get_password()

pr_base = 'https://gnats.juniper.net/web/default/%s'


class PRSpider(CrawlSpider):
    http_user = user
    http_pass = password
    name = 'pr'
    allowed_domains = ['gnats.juniper.net']

    def start_requests(self):

        pr_list = issues.find({'crawled': False}, {'number': 1})

        for url in map(lambda x: pr_base % x['number'], pr_list):
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        print('Crawling %s' % response.url)

        hxs = HtmlXPathSelector(response)

        return parse_gnats_item(hxs)
