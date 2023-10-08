import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CoursedetailSpider(CrawlSpider):
    name = "courseDetail"
    #allowed_domains = ["www.coventry.ac.uk"]
    start_urls = ["https://www.coventry.ac.uk/search/?search=&contentType=newcoursepage&csi=1679_"]


    #Creating links of courses
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//p[@class="h5 mtm"]/a'),
             callback="parse_item", follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="cd-pagination custom-buttons"]/li[@class="button"]/a'), follow=True),
        )

    
    def parse_item(self, response):

        # Giving the status when not available:
        entry_year = None
        study_mode = None
        duration = None
        course_code = None
        start_date = None
        #warranty = None



        #The variable called for the initial description box
        features = response.xpath('(//div[@class="feature-box"])')
        
        #loop for the initial description box value
        for feature in features:
            feature_name = feature.xpath('./p[@class="h3 mvn"]/text()').get().strip()
            if feature_name == "Year of entry":
                try:
                    entry_year = feature.xpath('./p[2]/text()').get()
                except:
                    entry_year = feature.xpath('//div[@class="radio-buttons -start"]/label/text()').get()
            elif feature_name == "Study mode":
                study_mode = feature.xpath('./p[2]/text()').get().strip()
            elif feature_name == "Duration":
                duration = feature.xpath('./p[2]').get().strip()
            elif feature_name == "Course code":
                course_code = feature.xpath('./p[2]/text()').get().strip()
            elif feature_name == "Start date":
                start_date = feature.xpath('./p[2]/text()').get().strip()

 
        
        yield{
            'courseName': response.xpath('//h1/text()').get().strip(),
            'location': response.xpath('//div[@class="feature-box location"]/p/span[@class="campus"]/text()').get().strip(),
            'fees': response.xpath('//td[@class="Fees-International-FullTime"]/text()').get().strip(),
            'url': response.url,
            'entry_year': entry_year,
            'study_mode': study_mode,
            'duration': duration,
            'course_code': course_code,
            'start_date': start_date
        }
        #item = {}
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        #return item
