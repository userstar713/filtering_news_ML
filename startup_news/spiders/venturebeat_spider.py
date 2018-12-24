from datetime import datetime, timedelta
import scrapy

from startup_news.items import Article
from startup_news.loaders import VentureBeatArticleLoader


class VentureBeatSpider(scrapy.Spider):

    name = "venturebeat"

    def start_requests(self):
        start_date = datetime(2006, 4, 17)

        date = start_date
        while date <= datetime.now():
            new_request = scrapy.Request(self.generate_url(date))
            new_request.meta["date"] = date
            new_request.meta["page_number"] = 1
            yield new_request
            date += timedelta(days=1)

    def generate_url(self, date, page_number=None):
        url = 'http://venturebeat.com/' + date.strftime("%Y/%m/%d") + "/"
        if page_number:
            url  += "page/" + str(page_number) + "/"
        return url

    def parse(self, response):
        date = response.meta['date']
        page_number = response.meta['page_number']

        # when I access a page number that doesn't exist I get 404
        # This gets around the infinite pagination
        if response.status == 200:
            articles = response.xpath('//h2[@class="article-title"]/a/@href').extract()
            for url in articles:
                request = scrapy.Request(url,
                                callback=self.parse_article)
                request.meta['date'] = date
                yield request

            url = self.generate_url(date, page_number+1)
            request = scrapy.Request(url,
                            callback=self.parse)
            request.meta['date'] = date
            request.meta['page_number'] = page_number
            yield request


    def parse_article(self, response):
        l = VentureBeatArticleLoader(Article(), response=response)
        l.add_xpath('title', '//h1/text()')
        l.add_xpath('text', '//div[@class="article-content"]//text()')
        l.add_xpath('tags', '//a[@rel="tag"]/text()')
        l.add_value('date', str(response.meta['date']))
        l.add_value('url', response.url)
        return l.load_item()
