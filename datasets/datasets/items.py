# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewsAllocineItem(scrapy.Item):
    
    title = scrapy.Field() # Le titre du film
    review = scrapy.Field() # Le commentaire
    stars = scrapy.Field() # La note donnée au film par l'auteur du commentaire


class NewsItem(scrapy.Item):

    headline = scrapy.Field()
    article = scrapy.Field()
    category = scrapy.Field()

class JobItem(scrapy.Item):

    title = scrapy.Field()
    description = scrapy.Field()
    company = scrapy.Field()
    keyword = scrapy.Field()
    posted_date = scrapy.Field()
    location = scrapy.Field()