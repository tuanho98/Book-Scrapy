import scrapy
from ..items import Scrapingbook2Item


class Book(scrapy.Spider):
    name = 'bookDetails'
    start_urls = ['https://www.barnesandnoble.com/b/books/best-books-of-the-year/best-books-of-the-year-2002/_/N-29Z8q8Z1qri'
                  ]

    def parse(self, response):
        items = Scrapingbook2Item()
        base = "https://www.barnesandnoble.com"
        links = response.css(".pImageLink::attr(href)").extract()
        i = 0
        while i < len(links):

            link = links[i]
            title = response.css('.pt-xs a::text').extract()[i]
            author = response.css('.product-shelf-author a::text').extract()[i]
            price = response.css('.format+ span::text').extract()[i]
            items['title'] = title
            items['author'] = author
            items['price'] = price
            print(link)
            i += 1
            print(i)
            url = base+link

            request = scrapy.Request(url,
                                     callback=self.parse_next,
                                     dont_filter=True,
                                     )
            request.meta['item'] = items
            yield request

    def parse_next(self, response):
        items = response.meta['item']
        items['star'] = "3333"

        yield items