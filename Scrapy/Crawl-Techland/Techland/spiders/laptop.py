import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LaptopSpider(CrawlSpider):
    name = "laptop"

    #Page initiation of first page
    start_urls = ["https://www.techlandbd.com/shop-laptop-computer/brand-laptops?limit=100&page=1"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="product-thumb"]/div[@class="caption"]/div[@class="name"]/a'), callback="parse_item", follow=True),
        
        #Next page generation
        Rule(LinkExtractor(restrict_xpaths='//a[@class="next"]'), follow=True)
    )

    def parse_item(self, response):
        # Giving the status when not available:
        product_price = None
        stock_status = None
        brand_name = None
        processor = None
        webcam = None
        warranty = None

        #The variable called for the initial description box
        features = response.xpath('(//div[@class="product-details"]/table/tbody/tr)')
        
        #loop for the initial description box value
        for feature in features:
            feature_name = feature.xpath('./td[1]/text()').get().strip()
            if feature_name == "product price":
                product_price = feature.xpath('./td[2]/text()').get().replace('৳','').replace(',','')
            elif feature_name == "Stock Status":
                stock_status = feature.xpath('./td[2]/text()').get()
            elif feature_name == "Brand":
                brand_name = feature.xpath('./td[2]/a/text()').get()
        
        #The variable called for the specification description box
        specifications = response.xpath('//div[@id="tab-specification"]//table/tbody/tr')
        
        #loop for the specificaton box value
        for specificaton in specifications:
            spec_title = specificaton.xpath('./td[1]/text()').get().strip()
            if spec_title == "Processor":
                processor = specificaton.xpath('./td[2]/text()').get()
            elif spec_title == "WebCam":
                webcam = specificaton.xpath('./td[2]/text()').get()
            elif spec_title == "Warranty":
                warranty = specificaton.xpath('./td[2]/text()').get()

        #Individual field with validation
        try:
            discount = int(response.xpath('//div[@class="module-item module-item-1 no-expand"]//span[@class="block-header-text"]/div/text()').get().replace('৳','').replace(',','').strip())
        except:
            discount = "Not Available"
        try:
            emi = int(response.xpath('//div[@class="module-item module-item-2 no-expand"]//span/text()').get().replace('৳','').replace(',','').strip())
        except:
            emi = "Not Available"

        yield{
            'brand' : brand_name,
            'title' : response.xpath('//div[@class="title page-title"]/text()').get().strip(),
            'stock_status' : stock_status,
            'product_price' : product_price,
            'cash_discount_price' : discount,
            'emi_price' : emi,
            'processor' : processor,
            'webcam' : webcam,
            'warranty' : warranty,
            'url' : response.url
        }
        
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        #return item
