import scrapy


class LaptopSpider(scrapy.Spider):
    name = "laptop"

    #Passing the url for the page of data
    start_urls = ["https://www.ryanscomputers.com/category/laptop-all-laptop?limit=100&osp=0"]

    #Function for the data extraction
    def parse(self, response):
        laptops = response.xpath('//div[@class="cus-col-2 cus-col-3 cus-col-4 cus-col-5 category-single-product mb-2 context1"]')
        
        #For loop for iterate all items
        for i, laptop in enumerate(laptops):
                    
            yield{
                'title': response.xpath(f'(//img[@class="card-img-top"]/@alt)[{i}]').get(),
                'href' : response.xpath(f'(//p[@class="card-text p-0 m-0 grid-view-text"]/a/@href)[{i}]').get(),
                'processor_Type' : response.xpath(f'(//li[contains(text(), "Processor")]/text())[{i}]').get(),
                'RAM' : response.xpath(f'(//li[contains(text(), "RAM")]/text())[{i}]').get(),
                'Proc_Generation' : response.xpath(f'(//li[contains(text(), "Generation")]/text())[{i}]').get(),
                'Display' : response.xpath(f'(//li[contains(text(), "Display")]/text())[{i}]').get()
            }
        
        #Calling Next Page
        next_page = response.xpath('//a[@aria-label="Next »"]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)