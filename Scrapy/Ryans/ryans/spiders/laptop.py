import scrapy


class LaptopSpider(scrapy.Spider):
    name = "laptop"

    #Passing the url for the page of data
    start_urls = ["https://www.ryanscomputers.com"]

    #Function for the data extraction
    def parse(self, response):
        
        
        #Calling Next Page
        next_page = response.xpath('//a[@aria-label="Next »"]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)