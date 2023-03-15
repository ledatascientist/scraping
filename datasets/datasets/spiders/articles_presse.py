from ..items import NewsItem
from scrapy import Request, Spider


class SpiderNews(Spider):
    name = "news"
    domain = "https://www.leparisien.fr/"

    categories = ["politique", "sports", "economie", "societe", "environnement", "faits-divers", "culture-loisirs"]

    def start_requests(self):
        for category in self.categories:
            for page in range(1,101):
                yield Request(f"{self.domain}{category}/{page}/", callback=self.parse_category, meta={'category': category})

    def parse_category(self, response):
        article_urls = response.css("div.flex-feed > div.story-preview > a::attr(href)").extract()
        for article_url in article_urls:
            if article_url.startswith("//www"):
                article_url = "https:" + article_url
            yield Request(article_url, callback=self.parse_article, meta=response.meta)
        

    def parse_article(self, response):

        sections = response.css("div.article-section section.content")
        headline = "\n".join(response.css("header.article_header > *::text").extract())
        article = "\n".join(["".join(section.css("p.paragraph *::text").extract()) for section in sections])

        item = NewsItem()

        item['category'] = response.meta['category']
        item['article'] = article
        item['headline'] = headline

        yield item