import scrapy
from bs4 import BeautifulSoup
from modul.SeleniumRequest import SeleniumRequest
from selenium.webdriver.support import expected_conditions
from selenium import webdriver
from selenium.webdriver.common.by import By
from modul.items import ModulItem

class KondicionerySpider(scrapy.Spider):
    name = 'kondicionery'
    allowed_domains = ['ek.ua']
    BASE_URL = 'https://ek.ua/ua'
    start_urls = ['https://hotline.ua/ua/bt/kondicionery/']

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse_tv,
                wait_time=10,
                wait_until=expected_conditions.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     ".model-shop-name .sn-div")
                ),
            )


    def parse_tv(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        kd_list = soup.find(id="list_form1").find_all('div')
        for kd in kd_list:
            try:
                img_url = kd.find(class_="list-img").find('img').get('src')
                model_wrapper = kd.find(class_="model-short-info").find(class_="model-short-title no-u")
                model = model_wrapper.find('span').getText()
                model_url = model_wrapper.get('href')
                price = kd.find(class_="model-hot-prices-td").find(class_="model-price-range").find('a').find_all(
                    'span'
                )
                start_price = int(price[0].getText().replace('\xa0', ''))
                end_price = int(price[1].getText().replace('\xa0', ''))
                shops = []
                shops_html = kd.find(class_="model-hot-prices").find_all('tr')
                for shop in shops_html:
                    shops.append(shop.find('u').getText())
            except AttributeError:
                continue
            yield ModulItem(
                model=model,
                model_url=f"{self.BASE_URL}{model_url}",
                start_price=start_price,
                end_price=end_price,
                img_url=img_url,
                image_urls=[img_url],
                shops=shops
            )
