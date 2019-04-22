# -*- coding: utf-8 -*-
import scrapy
import re
from paper.items import PaperItem
from scrapy.http import Request
import datetime
import time

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']
    def start_requests(self):
        url = 'https://www.tandfonline.com/toc/tgac20/%s/%s?nav=tocList'
        url_list = []
        for volume in range(34, 44):
            for issue in range(1,5):
                url_new = url % (volume,issue)
                url_list.append(scrapy.Request(url_new,dont_filter=True))
        return url_list
    def parse(self, response):
        paper_url = response.xpath('//a[@class="ref nowrap" ]/@href').extract()



        for i in paper_url:
            url = 'https://www.tandfonline.com' + i
            item = PaperItem()
            item['url'] = [url]
            print(url)
            yield Request(url=url,meta={'item':item},dont_filter=True,callback=self.parse_2)
    def parse_2(self,response):

        item2 = response.meta['item']
        #year
        #year = int(response.url.split('.')[-2])
        year = re.findall(r'\.(20\d{2})\.',response.url)[0]
        #title
        title = response.xpath('//span[@class ="NLM_article-title hlFld-title"]/text()').extract()
        if len(title) ==2 and title[0]==' ':
            title = title[1]
        else:
            title = title[0]
        #author,先得到所有作者的集合
        author_group = response.xpath('//span[@class="NLM_contrib-group"]')
        author_all = author_group.xpath('span')
        authors = []
        author_pos = 0
        for i in author_all:
            author_name = i.xpath('a/text()').extract()
            author_org = i.xpath('a/span/text()').extract()
            author_email = i.xpath('a/span/span/span[@class="corr-email"]/text()').extract()
            author = ''
            if len(author_name)!=0:
                author = {'name':author_name[0].strip(),'org':'','email':'','pos':author_pos}
            if len(author_org)!= 0:
                author['org'] = author_org[0].strip()
            if len(author_email) != 0:
                author['email'] = author_email[0].strip()
            author_pos+=1
            if author !='':
                if author['org']=='':
                    del author['org']
                if author['email'] == '':
                    del author['email']
                authors.append(author)
        print(authors)
        author_list = []
        for i in authors:
            author_list.append(i['name'])
        author_str = ','.join(author_list)
        #doi
        doi = response.xpath('//li[@class="dx-doi"]/a/@href').extract()
        #发表日期
        public_time = re.findall(r'Published online: (.+?)</div>',response.text)[0]
        #abstract
        abstract = response.xpath('//div[@class="abstractSection abstractInFull"]//text()').extract()
        #keywords
        keywords = a =response.xpath('//div[@class="hlFld-KeywordText"]//text()').extract()
        keyword = []
        for i in keywords:
            if i != ',\xa0' and i != 'Keywords: ':
                keyword.append(i)
        keyword_str = ''
        if len(keyword)!=0:
            keyword_str = ';'.join(keyword)
        #volume&issue&year
        a = response.xpath('//div[@class="title-container"]/h2//text()').extract()
        a = ''.join(a)
        volume = re.findall(r'Volume (\d+),',a)
        issue = re.findall(r'Issue \d',a)
        #page
        page_str = re.findall(r'Pages (\d+-\d+)',response.text)[0]
        page_start = page_str.split('-')[0]
        page_end = page_str.split('-')[1]
        item2['lang'] = 'en'
        # 论文的类别
        item2['venue'] = {'raw': 'Geodesy and Cartography', 'type': 1}
        item2['ts'] = datetime.datetime.now()
        # hash
        hashist = [word[0:1] for word in title.split()]
        ha = ''
        for i in hashist:
            ha += i
        item2['title'] = title
        item2['year'] = year
        if author_str !='':
            item2['author_str'] = author_str.strip()
        if len(authors)!=0:
            item2['authors'] = authors
        if len(doi)!=0:
            item2['doi'] = doi[0]
        if len(abstract)!= 0:
            if abstract[0] != "  ":
                item2['abstract'] = abstract[0]
        if len(volume)!=0:
            item2['volume'] = volume[0]
        if len(issue)!=0:
            item2['issue'] = volume[0]
        if keyword_str != '':
            item2['keywords'] = keyword_str
        item2['page_str'] = page_str
        item2['page_start'] = page_start
        item2['page_end'] = page_end
        item2['hash'] = ha
        item2['date_str'] = public_time
        item2['sid'] = response.url.split('/')[-1]
        item2['src'] = 'Taylor&Francis Online'
        yield item2