from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from gnats.spiders.utils import parse_gnats_item, get_password


user, password = get_password()

pr_base = 'https://gnats.juniper.net/web/default/%s'


class WorkerPrSpider(CrawlSpider):
    http_user = user
    http_pass = password
    name = 'worker_pr'
    allowed_domains = ['gnats.juniper.net']
    # parameters should not defined and set in __init__(), which will make the spider doesn't work with json api.
    # just set None here and use it in methods (as below).
    number = None
    uid = None

    def start_requests(self):
        url = pr_base % self.number
        yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        print('Crawling %s' % response.url)

        hxs = HtmlXPathSelector(response)

        item = parse_gnats_item(hxs)
        item['worker'] = [self.uid]
        return item
