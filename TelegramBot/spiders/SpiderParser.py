import scrapy
import urllib.response


class BrickSetSpider(scrapy.Spider):
    name = "Pavuk"

    def start_requests(self):
        urls = [
            f'http://poezdato.net/raspisanie-poezdov/{getattr(self, "url")}/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        SET_SELECTOR = 'tr'
        for brickset in response.css(SET_SELECTOR):
            TIME_SELECTOR = 'td ._time ::text'
            TYPE_SELECTOR = 'td ::attr(title)'
            PATH_SELECTOR = 'td a ::text'
            SHEDULE_SELECTOR = 'td a img ::attr(title)'
            if brickset.css(SHEDULE_SELECTOR) and "пригородный" in brickset.css(TYPE_SELECTOR).get().lower():
                yield {
                    'time': brickset.css(TIME_SELECTOR).getall(),
                    'path': brickset.css(PATH_SELECTOR)[1].get()[16::]+' '+brickset.css(PATH_SELECTOR)[2].get()[16::],
                    'schedule': brickset.css(SHEDULE_SELECTOR)[0].get(),
                }
