from ..items import JobItem
from urllib.parse import urljoin
from scrapy import Request, Spider

class SpiderIndeed(Spider):
    name = "jobs"
    domain = "https://fr.indeed.com/"
    keywords = ["data+science", "développement+web", "admin+système", "devops", "machine+learning"]
    headers = {'referer': domain}

    def start_requests(self):
        for keyword in self.keywords:
            url = f"{self.domain}emplois?q={keyword}&l=Rennes+(35)&radius=50"
            yield Request(url, callback=self.parse_results, headers=self.headers, meta={'keyword': keyword.replace("+", " ")})
    
    def parse_results(self, response):
        results = response.css("div.jobsearch-SerpJobCard")
        for result in results:
            url = result.css("h2.title a::attr(href)").extract_first()
            url = urljoin(self.domain, url)

            yield Request(url, callback=self.parse_description, meta=response.meta)
        
        # Pagination
        button_next = response.css("ul.pagination-list > li > a[aria-label=Suivant]")
        if button_next:
            url = urljoin(self.domain, button_next.css("::attr(href)").extract_first())
            yield Request(url, callback=self.parse_results, meta=response.meta)


    def parse_description(self, response):
        title = response.css("h1.jobsearch-JobInfoHeader-title::text").extract_first()
        subtitle = response.css("div.jobsearch-InlineCompanyRating > *::text").extract()
        company = subtitle[0]
        location = subtitle[-1]
        description = response.css("div.jobsearch-jobDescriptionText *::text").extract() 
        description = "\n".join(description)

        item = JobItem()

        item['title'] = title
        item['company'] = company
        item['location'] = location
        item['keyword'] = response.meta['keyword']
        item['description'] = description

        yield item

# TODO : Understand what, exactly, triggers the captcha and how to get around it.