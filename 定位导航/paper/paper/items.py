# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PaperItem(scrapy.Item):
    hash = scrapy.Field()
    authors = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    abstract = scrapy.Field()
    keywords = scrapy.Field()
    page_start = scrapy.Field()
    page_end = scrapy.Field()
    volume = scrapy.Field()
    issue = scrapy.Field()
    editor = scrapy.Field()
    author_str = scrapy.Field()
    oid = scrapy.Field()
    venue = scrapy.Field()
    isbn = scrapy.Field()
    issn = scrapy.Field()
    doi = scrapy.Field()
    url = scrapy.Field()
    citation = scrapy.Field()
    reference = scrapy.Field()
    raw_reference = scrapy.Field()
    src = scrapy.Field()
    sid = scrapy.Field()
    pdf_src = scrapy.Field()
    pdf = scrapy.Field()
    lang = scrapy.Field()
    year = scrapy.Field()
    ts = scrapy.Field()
    page_str = scrapy.Field()
    date_str =scrapy.Field()
