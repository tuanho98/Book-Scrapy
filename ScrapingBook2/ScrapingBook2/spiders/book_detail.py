import scrapy
from ..items import Scrapingbook2Item


class Book(scrapy.Spider):
    name = 'bookDetails'
    page_number = 2
    start_urls = ['https://www.barnesandnoble.com/b/books/best-books-of-the-year/best-books-of-the-year-2002/_/N-29Z8q8Z1qri?Nrpp=20&page=1'
                  ]

    def parse(self, response):

        base = "https://www.barnesandnoble.com"
        links = response.css(".pImageLink::attr(href)").extract()
        titles = response.css('.pt-xs a::text').extract()
        authors = response.css('.product-shelf-author a::text').extract()
        prices = response.css('.format+ span::text').extract()
        i = 0
        while i < len(links):
            items = Scrapingbook2Item()
            link = links[i]
            title = titles[i]
            author = authors[i]
            price = prices[i]
            items['title'] = title
            items['author'] = author
            items['price'] = price
            i += 1
            url = base+link
            print(url)
            request = scrapy.Request(url,
                                     callback=self.parse_next
                                     )
            request.meta['item'] = items
            yield request
        next_page = 'https://www.barnesandnoble.com/b/books/best-books-of-the-year/best-books-of-the-year-2002/_/N-29Z8q8Z1qri?Nrpp=20&page=' + \
            str(Book.page_number)
        if Book.page_number < 3:
            Book.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def parse_next(self, response):
        items = response.meta['item']
        items['star'] = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "bv_numReviews_text", " " ))]/text()'
                                       ).extract()
        yield items
