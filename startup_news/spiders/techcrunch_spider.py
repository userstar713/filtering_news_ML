from datetime import datetime, timedelta
import scrapy

from startup_news.items import Article
from startup_news.loaders import TechCrunchArticleLoader

#to run this use scrapy crawl techcrunch -o filename.csv

class TechCrunchSpider(scrapy.Spider):

    name = "techcrunch"

    def start_requests(self):
        start_date = datetime(2005, 6, 11)

        date = start_date
        while date <= datetime.now():
            new_request = scrapy.Request(self.generate_url(date))
            new_request.meta["date"] = date
            new_request.meta["page_number"] = 1
            yield new_request
            date += timedelta(days=1)


    def generate_url(self, date, page_number=None):
        url = 'https://techcrunch.com/' + date.strftime("%Y/%m/%d") + "/"
        if page_number:
            url  += "page/" + str(page_number) + "/"
        return url


    def parse(self, response):
        date = response.meta['date']
        page_number = response.meta['page_number']

        # when I access a page number that doesn't exist I get 404
        # I could use the pagination buttons, but this is less work
        if response.status == 200:
            articles = response.xpath('//h2[@class="post-title"]/a/@href').extract()
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
        l = TechCrunchArticleLoader(Article(), response=response)
        l.add_xpath('title', '//h1/text()')
        l.add_xpath('text', '//div[starts-with(@class,"article-entry text")]/p//text()')
        # l.add_xpath('text', '//div[@class="article-entry text"]/p//text()')
        l.add_xpath('tags', '//div[@class="loaded acc-handle"]/a/text()')
        l.add_value('date', str(response.meta['date']))
        l.add_value('url', response.url)
        return l.load_item()
