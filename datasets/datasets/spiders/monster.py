from ..items import JobItem
from urllib.parse import urljoin
from scrapy import Request, Spider

class SpiderMonster(Spider):
    name = "jobs_"
    domain = "https://fr.indeed.com/"
    keywords = ["data+science", "développement+web", "admin+système", "devops", "machine+learning"]
    headers = {'referer': domain}

    def start_requests(self):
        url = "https://www.monster.fr/emploi/q-emploi-informatique-et-technologie-de-l%E2%80%99information.aspx"
        
        yield Request(url, callback=self.parse_results)
    
    def parse_results(self, response):
        offers = response.css("div#SearchResults section[data-jobid]") 
        for offer in offers:
            url = offer.css("div.summary h2 a::attr(href)").extract_first()
            id_job = offer.css("::attr(data-jobid)").extract_first()

            response.meta['id_job'] = id_job

            yield Request(url, callback=self.parse_description, meta=response.meta)
        
        # Pagination
        # TODO

    def parse_description(self, response):
        # TODO

        item = JobItem()

        item['title'] = title
        item['company'] = company
        item['location'] = location
        item['keyword'] = response.meta['keyword']
        item['description'] = description

        yield item