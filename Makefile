CHECK=\033[32m✔\033[39m
DONE="\n$(CHECK) Done.\n"

PROJECT=gnats
SPIDER=gnats
TARGET=jcnrd
SERVER=http://scrapy.jcnrd.us
SCHEDULE=$(SERVER)/schedule.json 
ECHO=echo
SCRAPY=`which scrapy`
CURL=/usr/bin/curl


deploy:
	@$(ECHO) "\nDeploy $(PROJECT)..."
	@$(SCRAPY) deploy $(TARGET) -p $(PROJECT)
	@$(ECHO) $(DONE)

crawl:
	@$(ECHO) "\nCrawl $(SPIDER)..."
	@$(CURL) $(SCHEDULE) -d project=$(PROJECT) -d spider=$(SPIDER)

