import scrapy
from ..items import QuotesItem
import logging as log

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # start_urls = ["https://quotes.toscrape.com/"] # also can use below method

    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        log.info(f"Scraping: {response.url}")
        for quote in response.css("div.quote"):
            item = QuotesItem()
            item["title"] = quote.css("span.text::text").get()
            item["author"] = quote.css("small.author::text").get()
            item["author_details_link"] = response.urljoin(quote.css("span a::attr(href)").get())
            item["tags"] = quote.css("div.tags a.tag::text").getall()

            # Follow the author page, carrying the current item
            yield response.follow(
                item["author_details_link"],
                callback=self.parse_author_details,
                cb_kwargs = {"item": item},
                dont_filter = True
            )
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback = self.parse)

    def parse_author_details(self, response, item):
        log.info(f"Scraping author: {item['author']} details")
        item["author_details"] = {
            "born_date": response.css("span.author-born-date::text").get(),
            "born_location": response.css("span.author-born-location::text").get(),
            "bio": response.css("div.author-description::text").get()
        }
        yield item