from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
import requests

from mongodb import issues


from utils import parse_gnats_item, get_password

urlquote_safe = "%/:=?&"

user, password = get_password()

host = 'http://api.jcnrd.us'
api_monitored_members = host + '/directory/gnats-monitored-members.json'


responsible_base = 'https://gnats.juniper.net/web/default/do-query?adv=1&ignoreclosed=on&expr=%28%28%28arrival-date' \
                   + '+%3E+%222010-01-01%22%29+%26+%28%28dev-owner+%3D%3D+%22tchen%22%29+%7C+%28responsible+' \
                   + '%3D%3D+%22tchen%22%29%29%29+%26+%28last-modified+%3E+%221+years+ago%22%29%29+%26+%28' \
                   + 'builtinfield%3AState%5Btype%5D+%21%3D+%22closed%22%29&queryname=tchen%27s%2B' \
                   + 'responsible%2BPRs&recentPRs=lm2yr&colType=noscoped&csv=0&columns=synopsis%2Creported-in' \
                   + '%2Csubmitter-id%2Ccategory%2Cproblem-level%2Cblocker%2Cplanned-release%2Cstate%2Cresponsible' \
                   + '%2Coriginator%2Carrival-date%2Cbranch%2Ccustomer%2Ccustomer-escalation-owner%2Cdev-owner' \
                   + '%2Csystest-owner%2Clast-modified&op=%26'
pr_base = 'https://gnats.juniper.net/web/default/%s'


def format_url(uid):
    return responsible_base.replace('tchen', uid)


class ResponsibleSpider(CrawlSpider):
    http_user = user
    http_pass = password
    name = 'responsible'
    allowed_domains = ['gnats.juniper.net']

    rules = (
        Rule(SgmlLinkExtractor(
            allow=('/web/default/\d+',),
            deny=('edit')),
            callback='parse_item'
        ),
    )

    def init_crawled_status(self):
        issues.update({}, {'$set': {'crawled': False}}, multi=True)

    def start_requests(self):
        engineers = requests.get(api_monitored_members).json()

        self.init_crawled_status()

        for url in map(lambda x: format_url(x), engineers):
            yield self.make_requests_from_url(url)

    def parse_item(self, response):
        print('Crawling %s' % response.url)

        hxs = HtmlXPathSelector(response)

        return parse_gnats_item(hxs)
