CHECK=\033[32m✔\033[39m
DONE="\n$(CHECK) Done.\n"

PROJECT=gnats
RES_SPIDER=responsible
PR_SPIDER=pr
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

responsible:
	@$(ECHO) "\nCrawl $(RES_SPIDER)..."
	@$(CURL) $(SCHEDULE) -d project=$(PROJECT) -d spider=$(RES_SPIDER)

pr:
	@$(ECHO) "\nCrawl $(PR_SPIDER)..."
	@$(CURL) $(SCHEDULE) -d project=$(PROJECT) -d spider=$(PR_SPIDER)

