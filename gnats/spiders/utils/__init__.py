import base64
from gnats.items import GnatsItem
from dateutil.parser import parse
from pw import user, password

def get_text(hxs, xpath):
    try:
        return hxs.select('%s/text()' % xpath).extract()[0].strip()
    except:
        return ''


def parse_gnats_item(hxs):
    item = GnatsItem()
    item['number'] = get_text(hxs, '//*[@id="val_number"]')
    item['title'] = get_text(hxs, '//*[@id="val_synopsis"]')
    item['responsible'] = get_text(hxs, '//*[@id="val_responsible_1"]/a')
    item['state'] = get_text(hxs, '//*[@id="val_state_1"]')
    item['reported_in'] = get_text(hxs, '//*[@id="val_reported-in"]')
    item['submitter'] = get_text(hxs, '//*[@id="val_submitter-id"]')
    item['category'] = get_text(hxs, '//*[@id="val_category"]/a')
    item['level'] = get_text(hxs, '//*[@id="val_problem-level"]')
    item['platform'] = get_text(hxs, '//*[@id="val_platform"]')
    item['originator'] = get_text(hxs, '//*[@id="val_originator"]')
    item['customer'] = get_text(hxs, '//*[@id="val_customer"]')
    item['qa_owner'] = get_text(hxs, '//*[@id="val_systest-owner_1"]/a')
    item['ce_owner'] = get_text(hxs, '//*[@id="val_customer-escalation-owner"]/a')
    item['dev_owner'] = get_text(hxs, '//*[@id="val_dev-owner_1"]/a')
    item['audit_trail'] = hxs.select('//*[@id="audit-trail"]').extract()[0].strip()
    item['last_audit'] = get_text(hxs, '//*[@id="audit-trail"]//div[@class="section-contents"][last()]/pre')
    item['arrived_at'] = parse(get_text(hxs, '//*[@id="val_arrival-date"]'))
    item['modified_at'] = parse(get_text(hxs, '//*[@id="val_last-modified"]'))
    item['crawled'] = True
    item['comment'] = ''
    item['status'] = 'green'
    return item


def get_password():
    return user, base64.b64decode(password)