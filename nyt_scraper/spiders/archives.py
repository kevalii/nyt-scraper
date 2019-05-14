from scrapy import Spider
from nyt_scraper.items import HeadlineItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep


class ArchivesSpider(Spider):
    name = 'archives'
    start_urls = ['https://www.nytimes.com/search/?srchst=nyt']

    def __init__(self):
        ITER = 10000
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)

    def itemize(self, element):
        item = HeadlineItem()

        def safe_extract(attr, elements):
            try:
                item[attr] = elements[0].text
            except:
                item[attr] = 'ERR'
        safe_extract('category', element.find_elements_by_class_name(
            'css-myxawk'))
        safe_extract('headline', element.find_elements_by_tag_name('h4'))
        safe_extract('description', element.find_elements_by_class_name(
            'css-1dwgixl'))
        safe_extract('date', element.find_elements_by_tag_name('time'))

        return item

    def parse(self, response):
        self.driver.get(response.url)

        for i in range(100000):
            headlines = self.driver.find_elements_by_xpath(
                '//*[@data-testid="search-results"]/li[@data-testid="search-bodega-result"][position() >= last() - 9]')
            for headline in headlines:
                yield self.itemize(headline)

            next = self.driver.find_element_by_xpath(
                '//*[@id="site-content"]/div/div[2]/div[2]/div/button')
            sleep(0.5)

            try:
                next.click()
            except:
                break
