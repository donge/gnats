# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class GnatsItem(Item):
    number = Field()
    title = Field()
    responsible = Field()
    state = Field()
    reported_in = Field()
    submitter = Field()
    category = Field()
    level = Field()
    platform = Field()
    originator = Field()
    customer = Field()
    qa_owner = Field()
    ce_owner = Field()
    dev_owner = Field()
    audit_trail = Field()
    last_audit = Field()
    arrived_at = Field()
    modified_at = Field()
    crawled = Field()
