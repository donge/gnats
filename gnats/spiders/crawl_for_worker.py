from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from gnats.spiders.utils import parse_gnats_item, get_password
from mongodb import issues


user, password = get_password()

pr_base = 'https://gnats.juniper.net/web/default/%s'


class WorkerSpider(CrawlSpider):
    http_user = user
    http_pass = password
    name = 'worker'
    allowed_domains = ['gnats.juniper.net']
    number = None
    uid = None

    def __init__(self, number=None, uid=None):
        super(WorkerSpider, self).__init__()
        self.number = number
        self.uid = uid

    def start_requests(self):
        url = pr_base % self.number
        yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        print('Crawling %s' % response.url)

        hxs = HtmlXPathSelector(response)

        item = parse_gnats_item(hxs)
        item['worker'] = [self.uid]
        return item
