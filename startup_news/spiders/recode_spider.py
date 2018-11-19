from datetime import datetime, timedelta
from urlparse import urlparse
import scrapy

from startup_news.items import Article
from startup_news.loaders import RecodeArticleLoader

class RecodeSpider(scrapy.Spider):

    name = "recode"
    start_urls = [
        #the start of the recode archive
        "http://www.recode.net/archives/1"
    ]

    # the archive includes links to the verge and other sites, I skip those
    allowed_domains = [
        "recode.net"
    ]

    def parse(self, response):
        # this is pretty awful, I'm sorry
        # is_page ensures it won't keep requesting pages that don't exist
        # at this point it would have been simpler to just use the "next" button
        # meh it's already done
        is_page = False
        for url in response.xpath("//h2//a/@href").extract():
            parsed = urlparse(url)
            if "recode" in parsed.netloc:
                yield scrapy.Request(url, self.parse_article_recode)
            is_page = True
        # get the page number
        if is_page:
            url = response.url.split("/")
            url[-1] = str(int(url[-1]) + 1)
            next_page = "/".join(url)
            yield scrapy.Request(next_page, self.parse)

    def parse_article_recode(self, response):
        l = RecodeArticleLoader(Article(), response=response)
        l.add_xpath('title', '//h1/text()')
        l.add_xpath("subtitle", "//h2[contains(@class, 'c-entry-summary')]//text()")
        l.add_xpath('text', '//div[contains(@class,"c-entry-content")]/p//text()')

        # I do it in 2 steps because I don't know how to do this with a single xpath
        l.add_value('tags', response.xpath('//div[contains(@class, "c-entry-group-labels")]')[0].xpath(".//span/text()").extract())

        url = response.url.split("/")
        date = datetime(int(url[3]), int(url[4]), int(url[5]))
        l.add_value('date', str(date))

        l.add_value('url', response.url)
        return l.load_item()
