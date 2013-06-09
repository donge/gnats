from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from gnats.items import GnatsItem
from scrapy.selector import HtmlXPathSelector
import requests
import urllib
import base64
from dateutil.parser import parse

from password import user, password

urlquote_safe = "%/:=?&"

password = base64.b64decode(password)

host = 'http://directory-api.jcnrd.us'

exclude_sos_issue = '2010-01-01'
responsible_base = 'https://gnats.juniper.net/web/default/do-query?adv=0&arrival-date-since=' + \
                   exclude_sos_issue + \
                   '&OPT_dev-owner=EXACT&ignoreclosed=on&queryname=tchen%27s+responsible+PRs&dev-owner=%s' + \
                   '&recentPRs=lm2yr&colType=noscoped&csv=0&columns=synopsis%2Creported-in%2Csubmitter-id' + \
                   '%2Ccategory%2Cproblem-level%2Cblocker%2Cplanned-release%2Cstate%2Cresponsible' + \
                   '%2Coriginator%2Carrival-date%2Cbranch%2Ccustomer%2Ccustomer-escalation-owner' + \
                   '%2Cdev-owner%2Csystest-owner%2Clast-modified&op=%26'

pr_base = 'https://gnats.juniper.net/web/default/%s'


def format_url(uid):
    return urllib.quote(urllib.unquote(responsible_base) % uid, urlquote_safe).replace('&op=&', '')


class GnatsSpider(CrawlSpider):
    http_user = user
    http_pass = password
    name = 'gnats'
    allowed_domains = ['gnats.juniper.net']

    rules = (
        Rule(SgmlLinkExtractor(
            allow=('/web/default/\d+',),
            deny=('edit')),
            callback='parse_item'
        ),
    )


    def start_requests(self):
        teams = requests.get(host + '/gnats/monitored-group.json').json()
        engineers = []

        for team in teams:
            engineers += requests.get(host + '/groups/%s.json?uid=1' % team).json()['members']

        # yield self.make_requests_from_url(format_url('tchen'))
        for url in map(lambda x: format_url(x), engineers):
            yield self.make_requests_from_url(url)

    def get_text(self, hxs, xpath):
        try:
            return hxs.select('%s/text()' % xpath).extract()[0].strip()
        except:
            return ''

    def get_email_alias(self, hxs, xpath):
        data = self.get_text(hxs, xpath)
        if data:
            data = data.split('@')[0]
        return data

    def parse_item(self, response):
        print('Crawling %s' % response.url)

        hxs = HtmlXPathSelector(response)

        item = GnatsItem()
        item['number'] = self.get_text(hxs, '//*[@id="val_number"]')
        item['title'] = self.get_text(hxs, '//*[@id="val_synopsis"]')
        item['responsible'] = self.get_text(hxs, '//*[@id="val_responsible_1"]/a')
        item['state'] = self.get_text(hxs, '//*[@id="val_state_1"]')
        item['reported_in'] = self.get_text(hxs, '//*[@id="val_reported-in"]')
        item['submitter'] = self.get_text(hxs, '//*[@id="val_submitter-id"]')
        item['category'] = self.get_text(hxs, '//*[@id="val_category"]/a')
        item['level'] = self.get_text(hxs, '//*[@id="val_problem-level"]')
        item['platform'] = self.get_text(hxs, '//*[@id="val_platform"]')
        item['originator'] = self.get_text(hxs, '//*[@id="val_originator"]')
        item['customer'] = self.get_text(hxs, '//*[@id="val_customer"]')
        item['qa_owner'] = self.get_text(hxs, '//*[@id="val_systest-owner_1"]/a')
        item['ce_owner'] = self.get_text(hxs, '//*[@id="val_customer-escalation-owner"]/a')
        item['dev_owner'] = self.get_text(hxs, '//*[@id="val_dev-owner_1"]/a')
        item['audit_trail'] = hxs.select('//*[@id="audit-trail"]').extract()[0].strip()
        item['last_audit'] = self.get_text(hxs, '//*[@id="audit-trail"]//div[@class="section-contents"][last()]/pre')
        item['arrived_at'] = parse(self.get_text(hxs, '//*[@id="val_arrival-date"]'))
        item['modified_at'] = parse(self.get_text(hxs, '//*[@id="val_last-modified"]'))
        return item
