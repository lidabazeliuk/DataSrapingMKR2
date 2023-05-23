# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ModulItem(scrapy.Item):
    model=model,
    model_url=f"{self.BASE_URL}{model_url}",
    start_price=start_price,
    end_price=end_price,
    img_url=img_url,
    image_urls=[img_url],
    shops=shops