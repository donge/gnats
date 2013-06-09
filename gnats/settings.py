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

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'gnats (+http://www.yourdomain.com)'
