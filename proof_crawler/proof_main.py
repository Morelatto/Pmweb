import os
import time

from proof_crawler.spiders.proof_crawler import ProofSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


os.environ["SCRAPY_SETTINGS_MODULE"] = "proof_crawler.settings"
settings = get_project_settings()
# settings.set("LOG_FILE", "logs/[{0}] proof_crawler_log [{1}].txt".format(time.strftime("%d%m%Y"), time.strftime("%H%M%S")))
settings.set("LOG_LEVEL", "INFO")

process = CrawlerProcess(settings)

process.crawl(ProofSpider, info="")
process.start()
