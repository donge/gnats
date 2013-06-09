# Scrapy settings for gnats project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'gnats'

SPIDER_MODULES = ['gnats.spiders']
NEWSPIDER_MODULE = 'gnats.spiders'

ITEM_PIPELINES = [
    'gnats.pipelines.MongoPipeline',
]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': 1000,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = '''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.31
                (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31'''
